# Figma design vs Android app — Applitools Eyes + Python

Compares a **Figma frame** with the **real Android app screen**. The Figma frame is exported to Eyes with the Applitools Eyes Figma plugin and becomes the baseline. The test opens the app with Appium, the Native Mobile Library (NML) captures the screen, and Eyes compares it with the Figma frame.

```
Step 2  Figma ── Applitools Eyes plugin ── "Export to Eyes" ──▶ baseline
                 (app name, test name = frame name, Baseline name)

Step 5  pytest ── Appium + NML ── app screen ──▶ Eyes compares it with that baseline
                 (same app name, test name, step name, Baseline name)
```

Sample app: `app/Accessibility_static_xmllayout.apk` — Applitools sample app with the NML library built in.

## Requirements

- Python 3.9+
- Node.js and Appium 2: `npm i -g appium && appium driver install uiautomator2`
- an Android emulator (Android Studio)
- An Applitools API key (Eyes → your profile → My API key)
- Figma, with permission to run the Applitools Eyes plugin

## Step 1: Install

```
cd android
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APPLITOOLS_API_KEY=<your Applitools API key>
```

## Step 2: Export the Figma frames with the Eyes plugin

1. In Figma, select the frames to compare. Each frame becomes its own Eyes test.
2. Open **Plugins → Applitools Eyes** and paste your API key. Server URL: `https://eyes.applitools.com`.
3. Check the settings:
   - **App name**: by default `<Figma file name> - <Figma page name>`.
   - **Test name**: the frame name.
   - **Match level**: Layout.
4. Click **Export to Eyes**.
5. Open **Eyes configuration details** and copy the **Baseline name** of each frame.

The frames in this sample:

| Figma frame (= Eyes test) | `fully` | Size |
|---|---|---|
| `Android / Main Screen` | `True` — Android NML always captures the full scrollable screen | 411×1898 |

## Step 3: Put the Figma values in `figma_config.py`

- `APP_NAME` = the plugin's App name.
- For each frame in `FRAMES`: `frame` = the frame name, `baseline_env_name` = the Baseline name you copied.

The app name, frame name and Baseline name must match exactly. If one is different, Eyes creates a new baseline from the app screen instead of comparing it with Figma.

Frame names with `/` (for example `iOS / Main Screen`) are fine: the test uses `-` in the step name, because the iOS NML library saves each screenshot to a file named after the step. Eyes pairs the step with the Figma frame by order, so it still compares.

## Step 4: Start Appium and the device

```
appium            # in its own terminal, http://127.0.0.1:4723
```

```
emulator -list-avds
emulator -avd Pixel_9 &        # or start it from Android Studio
adb devices                    # shows the emulator id
```

## Step 5: Run the test

```
AVD_NAME=Pixel_9 PLATFORM_VERSION=16 pytest test_figma_android.py
```

The test opens the app, and for each frame in `figma_config.py` it captures the screen and compares it with the Figma frame. It prints one Eyes link per frame.

## Step 6: Review the result in Eyes

Open the link. **Unresolved** means Eyes found differences between the app and the Figma frame; they are highlighted on the screen. Review them, then accept (thumbs up) or reject (thumbs down) each one.

## Match level

| `MATCH_LEVEL` | What it reports | Use it for |
|---|---|---|
| `LAYOUT` (default) | Position and structure of elements; ignores text content and colours | "Does the app follow the design's layout?" — the best start for Figma vs app |
| `STRICT` | Any visible difference, including font rendering (Figma fonts vs the device fonts) | Content and pixel checks — expect font noise unless the design uses the device fonts |

`MATCH_LEVEL=STRICT AVD_NAME=Pixel_9 PLATFORM_VERSION=16 pytest test_figma_android.py`

## Using your own app and design

1. Your app needs the **Applitools NML library built in** (as the sample app has). See the Applitools docs for adding NML to an Android app.
2. In Figma, make one frame per screen at the device size, for example 411×1898 for this sample (dp, full scrollable height). Android NML captures in dp and always captures the full scrollable screen, so make the Figma frame as tall as the content.
3. Export the frames (Step 2) and add one `FRAMES` entry per frame (Step 3).
4. Open the screen in the test before the check (tap, navigate, wait), then run with your app:

```
APP_PATH=/path/to/your-app.apk pytest test_figma_android.py
```

## No plugin access? Use the Figma REST API instead

`figma_baseline.py` does Step 2 without the plugin. It exports each frame as a PNG through the Figma REST API and uploads it with the Eyes Images SDK, with the same names as the plugin. While `baseline_env_name` is still the placeholder, it uses `Figma | <frame name>`, and the test does the same.

Requirement: a Figma personal access token (Figma → Settings → Security → Personal access tokens, scope `file_content:read`), and each frame's `node_id` in `figma_config.py` (`node-id=1-28` in the Figma URL → `"1:28"`). Put the token in a `.env` file in this folder (git-ignored):

```
FIGMA_ACCESS_TOKEN=figd_...
```

```
python figma_baseline.py
```

## Files

| File | Purpose |
|---|---|
| `figma_config.py` | App name, and per Figma frame: name, Baseline name, capture mode |
| `test_figma_android.py` | The test: one Eyes check per Figma frame |
| `conftest.py` | Appium driver with NML, and Eyes pointed at the Figma baseline |
| `figma_baseline.py` | Step 2 without the plugin (Figma REST API) |
| `app/` | Sample app with NML built in |
