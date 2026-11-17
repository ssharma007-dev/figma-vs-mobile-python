# Figma vs iOS app — execution steps

Requirement: the Figma frames are already exported to the Eyes Dashboard with the Applitools Eyes Figma plugin.

Requirement: Python 3.9+, Node.js, and an iOS Simulator (Xcode).

## Step 1: Install

```
cd ios
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm i -g appium
appium driver install xcuitest
```

## Step 2: Set your Applitools API key

```
export APPLITOOLS_API_KEY=<your Applitools API key>
```

## Step 3: Add the Figma values to `figma_config.py`

Copy these from the Figma export (plugin → **Eyes configuration details**):

- `APP_NAME` = the App name.
- For each frame in `FRAMES`:
  - `frame` = the frame name (the test name in Eyes).
  - `baseline_env_name` = the Baseline name.

The values must match exactly. If one is different, Eyes saves the app screen as a new baseline instead of comparing it with the Figma frame.

## Step 4: Start Appium

In a separate terminal:

```
appium
```

## Step 5: Start the iOS device

```
xcrun simctl list devices available | grep iPhone     # copy the UDID of a Simulator
xcrun simctl boot <simulator udid>
open -a Simulator
```

## Step 6: Run the test

```
IOS_UDID=<simulator udid> PLATFORM_VERSION=<iOS version> pytest test_figma_ios.py
```

Example:

```
IOS_UDID=258C9CC4-4C21-44CB-903B-AEA4C056B484 PLATFORM_VERSION=18.0 pytest test_figma_ios.py
```

The test opens the sample app in `app/`, captures the screen for each frame in `figma_config.py`, and compares it with the Figma frame. To run your own app, add `APP_PATH=/path/to/your/app` in front of the command.

## Step 7: See the result

The test prints one Eyes link per frame. Open it in the Eyes Dashboard:

- **Passed**: the app screen matches the Figma frame.
- **Unresolved**: Eyes found differences; they are highlighted on the screen. Accept (thumbs up) or reject (thumbs down) each one.
