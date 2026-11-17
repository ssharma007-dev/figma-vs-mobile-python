# Figma vs mobile app — execution steps

Requirement: the Figma frames are already exported to the Eyes Dashboard with the [Applitools Eyes Figma plugin](https://www.applitools.com/docs/eyes/integrations/design-validation/figma-plugin), and you have the **Baseline name** of each frame. After the export, the plugin shows it under **Eyes configuration details**. Copy it into `baseline_env_name` in `figma_config.py`.

Requirement: Appium is running (`appium`), the iOS Simulator or Android emulator is started, and the Figma values are in `figma_config.py`. The README in [`ios/`](ios) or [`android/`](android) shows how.

## Step 1: Install

```
cd ios                     # or: cd android
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APPLITOOLS_API_KEY=<your Applitools API key>
```

## Step 2: Run the test

Choose how the app screen is captured with `CAPTURE`:

- `CAPTURE=nml`: the Applitools Native Mobile Library (NML) inside the app captures the screen. This is the default.
- `CAPTURE=sdk`: the Eyes Appium SDK captures the screen with an Appium screenshot. The status bar is cropped, so these use their own Figma frames (`"sdk"` in `figma_config.py`).

**iOS — NML** (in `ios/`)

```
CAPTURE=nml IOS_UDID=<simulator udid> PLATFORM_VERSION=<iOS version> pytest test_figma_ios.py
```

**iOS — SDK** (in `ios/`)

```
CAPTURE=sdk IOS_UDID=<simulator udid> PLATFORM_VERSION=<iOS version> pytest test_figma_ios.py
```

**Android — NML** (in `android/`)

```
CAPTURE=nml AVD_NAME=<avd name> PLATFORM_VERSION=<Android version> pytest test_figma_android.py
```

**Android — SDK** (in `android/`)

```
CAPTURE=sdk AVD_NAME=<avd name> PLATFORM_VERSION=<Android version> pytest test_figma_android.py
```

Example:

```
CAPTURE=nml AVD_NAME=Pixel_9 PLATFORM_VERSION=16 pytest test_figma_android.py
```

To run your own app instead of the sample in `app/`, add `APP_PATH=/path/to/your/app` in front of the command.

## Step 3: See the result

The test prints one Eyes link per Figma frame. Open it in the Eyes Dashboard:

- **Passed**: the app screen matches the Figma frame.
- **Unresolved**: Eyes found differences; they are highlighted on the screen. Accept (thumbs up) or reject (thumbs down) each one.
