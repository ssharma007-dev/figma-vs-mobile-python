"""
Step 1 — Figma design → Applitools Eyes baseline (Python)

Exports each mobile frame from Figma as a PNG (Figma REST API) and uploads it
to Eyes with the Images SDK. Each design becomes the baseline for one
app/test/step under a fixed baseline environment name, which the NML device
tests (step 2, `pytest`) reuse so Eyes compares the device screen to the design.

ENV VARS (or .env file next to this script):
  FIGMA_ACCESS_TOKEN     — Figma personal access token (file_content:read)
  APPLITOOLS_API_KEY     — Applitools API key
  APPLITOOLS_SERVER_URL  — optional; defaults to the Applitools public cloud

USAGE:
  python figma_baseline.py            # all platforms in DESIGNS
  python figma_baseline.py ios        # one platform
"""
import json
import os
import sys
import urllib.request

from applitools.images import BatchInfo, Configuration, Eyes, Target

from figma_config import APP_NAME, DESIGNS, FIGMA_FILE_KEY

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(HERE, "figma_exports")


def load_dotenv():
    path = os.path.join(HERE, ".env")
    if os.path.exists(path):
        for line in open(path):
            key, sep, value = line.strip().partition("=")
            if sep and not key.startswith("#"):
                os.environ.setdefault(key, value)


def figma_get(url, token):
    request = urllib.request.Request(url, headers={"X-Figma-Token": token})
    with urllib.request.urlopen(request) as response:
        return response.read()


def export_frames(designs, token):
    # scale=1 → 1 Figma unit = 1 image pixel, matching NML's point/dp-sized captures.
    steps = [step for design in designs.values() for step in design["steps"]]
    url = "https://api.figma.com/v1/images/{}?ids={}&format=png&scale=1".format(
        FIGMA_FILE_KEY, ",".join(step["node_id"] for step in steps))
    image_urls = json.loads(figma_get(url, token))["images"]

    os.makedirs(EXPORT_DIR, exist_ok=True)
    paths = {}
    for step in steps:
        path = os.path.join(EXPORT_DIR, step["node_id"].replace(":", "-") + ".png")
        with open(path, "wb") as f:
            f.write(figma_get(image_urls[step["node_id"]], token))
        paths[step["node_id"]] = path
        print("Exported Figma node {} → {}".format(step["node_id"], path))
    return paths


def upload_baseline(platform, design, paths):
    config = Configuration()
    config.set_api_key(os.environ["APPLITOOLS_API_KEY"])
    if os.getenv("APPLITOOLS_SERVER_URL"):
        config.set_server_url(os.environ["APPLITOOLS_SERVER_URL"])
    config.set_batch(BatchInfo("Figma Baselines | " + APP_NAME))
    config.set_baseline_env_name(design["baseline_env_name"])
    # Re-running after a design change replaces the baseline with the new frame.
    config.set_save_diffs(True)

    eyes = Eyes()
    eyes.set_configuration(config)
    try:
        eyes.open(APP_NAME, design["test_name"])
        for step in design["steps"]:
            eyes.check(step["name"], Target.image(paths[step["node_id"]]))
        results = eyes.close(raise_ex=False)
        print("[{}] {} → {}".format(platform, "new baseline" if results.is_new else results.status, results.url))
    finally:
        eyes.abort()


def main():
    load_dotenv()
    platforms = sys.argv[1:] or list(DESIGNS)
    designs = {p: DESIGNS[p] for p in platforms}
    paths = export_frames(designs, os.environ["FIGMA_ACCESS_TOKEN"])
    for platform, design in designs.items():
        upload_baseline(platform, design, paths)


if __name__ == "__main__":
    main()
