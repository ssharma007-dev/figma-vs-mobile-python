# Figma vs Android app — execution steps

Requirement: the Figma frames are already exported to the Eyes Dashboard with the [Applitools Eyes Figma plugin](https://www.applitools.com/docs/eyes/integrations/design-validation/figma-plugin), and you have the **Baseline name** of each frame. After the export, the plugin shows it under **Eyes configuration details**. Copy it into `baseline_env_name` in `figma_config.py`.

Export from Figma: **Plugins → Applitools Eyes → Export to Eyes**.

<img src="../docs/screenshots/figma-plugin-export.png" alt="Applitools Eyes Figma plugin" width="360">

After the export, open **Eyes configuration details** and copy the **Baseline name** (for example `Frame1_685`).

<img src="../docs/screenshots/figma-plugin-baseline-name.png" alt="Baseline name in Eyes configuration details" width="360">

Requirement: Python 3.9+, Node.js, and an Android emulator (Android Studio).

## Sample values

| Value | Where it comes from | Sample value |
|---|---|---|
| `APPLITOOLS_API_KEY` | Eyes Dashboard → your profile → My API key | `aBcD1234...` |
| `APP_NAME` | Figma plugin → App name | `NML Python – Figma vs Mobile (demo) - Page 1` |
| `frame` | Figma frame name (= test name in Eyes) | `Android / Main Screen` |
| `baseline_env_name` | Figma plugin → Eyes configuration details → Baseline name | `Frame1_685` (`Figma \| Android / Main Screen` in the sample below) |
| `fully` | `False`: visible screen only, `True`: full scrollable screen | `True` |
| `AVD_NAME` | `emulator -list-avds` | `Pixel_9` |
| `PLATFORM_VERSION` | Simulator / emulator OS version | `16` |
| `CAPTURE` | How the screen is captured | `nml` or `sdk` |

Your values come from your own Figma export; the Baseline name is whatever the plugin shows for each frame.

Sample `figma_config.py`:

```python
APP_NAME = "NML Python – Figma vs Mobile (demo) - Page 1"

FRAMES = {
    "nml": [
        {"frame": "Android / Main Screen", "baseline_env_name": "Figma | Android / Main Screen",
         "node_id": "2:2", "fully": True},
    ],
    "sdk": [
        {"frame": "SDK / Android / Viewport", "baseline_env_name": "Figma | SDK / Android / Viewport",
         "node_id": "4:142", "fully": False},
    ],
}
```

## Step 1: Install

```
cd android
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm i -g appium
appium driver install uiautomator2
```

## Step 2: Set your Applitools API key

```
export APPLITOOLS_API_KEY=<your Applitools API key>
```

## Step 3: Add the Figma values to `figma_config.py`

Copy these from the Figma export (plugin → **Eyes configuration details**):

- `APP_NAME` = the App name.
- For each frame in `FRAMES["nml"]` (NML capture) and `FRAMES["sdk"]` (SDK capture):
  - `frame` = the frame name (the test name in Eyes).
  - `baseline_env_name` = the Baseline name.

The values must match exactly. If one is different, Eyes saves the app screen as a new baseline instead of comparing it with the Figma frame.

## Step 4: Start Appium

In a separate terminal:

```
appium
```

## Step 5: Start the Android device

```
emulator -list-avds
emulator -avd <avd name> &
adb devices                    # the emulator shows as "device"
```

## Step 6: Run the test

```
CAPTURE=nml AVD_NAME=<avd name> PLATFORM_VERSION=<Android version> pytest test_figma_android.py
CAPTURE=sdk AVD_NAME=<avd name> PLATFORM_VERSION=<Android version> pytest test_figma_android.py
```

- `CAPTURE=nml` (default): the Applitools Native Mobile Library inside the app captures the screen.
- `CAPTURE=sdk`: the Eyes Appium SDK captures an Appium screenshot (status bar cropped).

Example:

```
CAPTURE=nml AVD_NAME=Pixel_9 PLATFORM_VERSION=16 pytest test_figma_android.py
```

The test opens the sample app in `app/`, captures the screen for each frame in `figma_config.py`, and compares it with the Figma frame. To run your own app, add `APP_PATH=/path/to/your/app` in front of the command.

## Step 7: See the result

The test prints one Eyes link per frame. Open it in the Eyes Dashboard:

- **Passed**: the app screen matches the Figma frame.
- **Unresolved**: Eyes found differences; they are highlighted on the screen. Accept (thumbs up) or reject (thumbs down) each one.

<img src="../docs/screenshots/eyes-baseline-vs-checkpoint-android.png" alt="Android: Figma baseline vs app checkpoint" width="560">

The baseline is the Figma frame; the checkpoint is the app screen. Here Checklist shows `0/4` in Figma and `1/4` in the app, and the test still passes: Layout checks position and structure, not text. Use `MATCH_LEVEL=STRICT` to catch text and colour differences too.
