# Figma design vs mobile app — Applitools NML + Python

Compares a **Figma mobile design** with the **real iOS / Android app screen** captured by the Native Mobile Library (NML), using only Python.

> Applitools' built-in [Figma Dev Comparison](https://applitools.com/docs/eyes/integrations/design-validation/figma-dev-compare) (`set_figma_baselines`) supports web SDKs only — native mobile is "planned for a future release". This project does the same job for Appium today: the Figma frame is uploaded as the Eyes baseline, and the NML checkpoint is compared against it.

## How it works

```
Step 1  figma_baseline.py
        Figma REST API ──PNG──▶ Eyes Images SDK ──▶ baseline
                                 (app, test, step, baseline_env_name)

Step 2  pytest
        Appium + NML ──screen──▶ Eyes Selenium SDK ──▶ compared to that baseline
                                 (same app, test, step, baseline_env_name)
```

The link between the two is `figma_config.py`: both steps use the **same app name, test name, step name and `baseline_env_name`**. `baseline_env_name` is what lets a screenshot from an iPhone/Pixel compare against an image that came from Figma.

## Setup

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`.env` (git-ignored):

```
FIGMA_ACCESS_TOKEN=figd_...       # Figma → Settings → Security → Personal access tokens (file_content:read)
```

and `APPLITOOLS_API_KEY` in your environment.

Sample app (from the `main` branch of this repo):

```
git clone --depth 1 --branch main https://github.com/applitools/nml-plug-and-play.git nml-main
cp -R nml-main/static_instrumented_sample_application ./static_instrumented_sample_application
rm -rf nml-main
```

## Run

```
# Step 1 — upload the Figma designs as baselines (re-run whenever the design changes)
python figma_baseline.py            # all designs, or e.g.: python figma_baseline.py nml_ios nml_android

# Step 2 — compare the app against them (Appium server + emulator/Simulator running)
pytest tests/nml/test_figma_android_nml.py
IOS_UDID=<simulator udid> pytest tests/nml/test_figma_ios_nml.py

# Optional — classic Appium screenshots instead of NML
pytest tests/sdk
```

## Match level

| `MATCH_LEVEL` | What it reports | Use it for |
|---|---|---|
| `STRICT` | Any visible difference, including font rendering (Figma fonts vs SF Pro / Roboto on device) | Catching content and pixel differences — expect noise unless the design uses the device fonts |
| `LAYOUT` (default) | Structure and position of elements only; ignores text content and colours | "Does the build follow the design's layout?" |

## Viewport and full page

| Platform | Steps | Figma frame |
|---|---|---|
| iOS | `Main Screen | Viewport` (`fully(False)`) and `Main Screen | Full Page` (`fully()`) | 393×852 and 393×2056 |
| Android | `Main Screen | Full Page` | 411×1898 (Android NML always captures the full scrollable screen) |

## Known limitation: match regions with NML

Coded regions (`.ignore(...)`, `.strict(...)`, `.layout(...)`) are **dropped on the NML capture path** (verified with eyes-selenium 6.5.21 / core-universal 4.76: the SDK sends the region, the core's check settings arrive empty). So "Layout for the screen + Strict on key content" is not possible with NML today.

`tests/sdk/` runs the same screens with classic Appium screenshots, where regions *are* applied. Classic captures crop the status bar (≈53pt iOS / ≈54dp Android), so they use their own Figma frames and baselines (`sdk_ios`, `sdk_android` in `figma_config.py`); classic Android doesn't scroll this screen, so it is viewport only.

## Using your own design

1. In Figma, make one frame per screen at the device's **point / dp size** — e.g. 393×852 for iPhone 15/16 Pro. NML captures in points (iOS) and dp (Android), so `scale=1` exports line up 1:1.
   - Android `Target.window()` captures the full scrollable screen, so make the Android frame as tall as the content.
2. Put each frame's node id (`node-id=1-28` in the URL → `"1:28"`) in `figma_config.py`.
3. Add a `DESIGNS` entry per screen, and a matching `eyes.check(step_name, ...)` in the test.

## Files

| File | Purpose |
|---|---|
| `figma_config.py` | Figma file/node ids and the shared Eyes identifiers |
| `figma_baseline.py` | Step 1 — export Figma frames, upload as baselines |
| `conftest.py` | Step 2 — Appium + NML drivers and the Eyes fixture pointed at the Figma baseline |
| `tests/figma_check.py` | Opens Eyes and checks one step per Figma frame, in upload order |
| `tests/nml/`, `tests/sdk/` | One test per platform — NML capture, or classic Appium screenshot |
