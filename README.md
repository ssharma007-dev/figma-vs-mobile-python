# Figma design vs mobile app — Applitools NML + Python

Compares a **Figma mobile design** with the **real iOS / Android app screen** captured by the Native Mobile Library (NML), using only Python.

For native mobile apps, the Figma frame is exported to Eyes with the **Applitools Eyes Figma plugin**, and the app screen captured by NML is compared against it. ([Figma Dev Comparison](https://applitools.com/docs/eyes/integrations/design-validation/figma-dev-compare) with `set_figma_baselines` is the web SDK flow.)

## How it works

```
Step 1  Figma ── Applitools Eyes plugin ── "Export to Eyes" ──▶ baseline
                 (app name, test name = frame name, Baseline name)

Step 2  pytest
        Appium + NML ──screen──▶ Eyes Selenium SDK ──▶ compared to that baseline
                                 (same app name, test name, step name, Baseline name)
```

The link between the two is `figma_config.py`. The device test uses the **same app name, test name, step name and Baseline name** as the plugin export. The Baseline name (`set_baseline_env_name`) is what lets a screenshot from an iPhone/Pixel compare against an image that came from Figma.

## Setup

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APPLITOOLS_API_KEY=<your Applitools API key>
```

Sample app (from the `main` branch of nml-plug-and-play):

```
git clone --depth 1 --branch main https://github.com/applitools/nml-plug-and-play.git nml-main
cp -R nml-main/static_instrumented_sample_application ./static_instrumented_sample_application
rm -rf nml-main
```

## Step 1: Export the Figma frames with the Eyes plugin

Requirement: permission to run the Applitools Eyes plugin in your Figma workspace.

1. In Figma, select the frames to export. Each frame becomes its own Eyes test.
2. Open **Plugins → Applitools Eyes**, and paste your API key. Server URL: `https://eyes.applitools.com`.
3. Check the settings:
   - **App name**: by default `<Figma file name> - <Figma page name>`. Put the same value in `APP_NAME` in `figma_config.py`.
   - **Test name**: the frame name. Put it in `frame` in `figma_config.py`. The step name is the frame name too.
   - **Match level**: Layout is a good start for design vs app (see below).
4. Click **Export to Eyes**.
5. Open **Eyes configuration details**, copy the **Baseline name** for each frame, and paste it into `baseline_env_name` in `figma_config.py`.

Re-export whenever the design changes.

## Step 2: Compare the app with the Figma frames

Requirement: a running Appium server (`appium`) and a booted emulator or Simulator.

```
pytest tests/nml/test_figma_android_nml.py
IOS_UDID=<simulator udid> pytest tests/nml/test_figma_ios_nml.py
```

Each test opens Eyes once per frame, with the frame's Baseline name, and prints the result link.

Optional: `pytest tests/sdk` runs the same check with classic Appium screenshots instead of NML (see the regions note below).

## No plugin access? Use the Figma REST API instead

`figma_baseline.py` does Step 1 without the plugin. It exports each frame as a PNG through the Figma REST API and uploads it with the Eyes Images SDK, using the same names as the plugin (test name = step name = frame name). While `baseline_env_name` still holds the placeholder, it uses `Figma | <frame name>`, and the device test does the same.

Requirement: a Figma personal access token (Figma → Settings → Security → Personal access tokens, scope `file_content:read`), in a git-ignored `.env`:

```
FIGMA_ACCESS_TOKEN=figd_...
```

```
python figma_baseline.py                        # every frame in figma_config.py
python figma_baseline.py nml_ios nml_android    # some platforms
```

## Match level

| `MATCH_LEVEL` | What it reports | Use it for |
|---|---|---|
| `STRICT` | Any visible difference, including font rendering (Figma fonts vs SF Pro / Roboto on device) | Catching content and pixel differences — expect noise unless the design uses the device fonts |
| `LAYOUT` (default) | Structure and position of elements only; ignores text content and colours | "Does the build follow the design's layout?" |

## Viewport and full page

| Platform | Figma frame (= Eyes test) | Capture | Size |
|---|---|---|---|
| iOS | `iOS / Main Screen` | `fully: False` (visible screen) | 393×852 |
| iOS | `iOS / Main Screen \| Full` | `fully: True` (full scrollable screen) | 393×2056 |
| Android | `Android / Main Screen` | `fully: True` (Android NML always captures the full scrollable screen) | 411×1898 |

## Known limitation: match regions with NML

Coded regions (`.ignore(...)`, `.strict(...)`, `.layout(...)`) are **dropped on the NML capture path** (verified with eyes-selenium 6.5.21 / core-universal 4.76: the SDK sends the region, the core's check settings arrive empty). So "Layout for the screen + Strict on key content" is not possible with NML today.

`tests/sdk/` runs the same screens with classic Appium screenshots, where regions *are* applied. Classic captures crop the status bar (≈53pt iOS / ≈54dp Android), so they use their own Figma frames (`sdk_ios`, `sdk_android` in `figma_config.py`); classic Android doesn't scroll this screen, so it is viewport only.

## Using your own design

1. In Figma, make one frame per screen at the device's **point / dp size**, for example 393×852 for iPhone 15/16 Pro. NML captures in points (iOS) and dp (Android), so the frame and the screen line up 1:1.
   - Android NML captures the full scrollable screen, so make the Android frame as tall as the content.
2. Add one entry per frame to `FRAMES` in `figma_config.py`: the frame name, the Baseline name from the plugin, and `fully`.
   - `node_id` is only needed for `figma_baseline.py` (`node-id=1-28` in the Figma URL → `"1:28"`).
3. Export the frames with the plugin (Step 1) and run the test for that platform (Step 2).

## Files

| File | Purpose |
|---|---|
| `figma_config.py` | App name, and per frame: name, Baseline name, capture mode |
| `figma_baseline.py` | Step 1 without the plugin — Figma REST API → Eyes Images SDK |
| `conftest.py` | Step 2 — Appium + NML drivers and the Eyes fixture pointed at the Figma baseline |
| `tests/figma_check.py` | One Eyes test per Figma frame, named like the plugin export |
| `tests/nml/`, `tests/sdk/` | One test per platform — NML capture, or classic Appium screenshot |
