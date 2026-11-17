# Figma vs Android app — execution steps

Requirement: the Figma frames are already exported to the Eyes Dashboard with the Applitools Eyes Figma plugin.

Requirement: Python 3.9+, Node.js, and an Android emulator (Android Studio).

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
