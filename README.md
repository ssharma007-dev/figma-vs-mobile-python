# Figma design vs mobile app — Applitools Eyes + Python

Compare **Figma frames** with the **real iOS and Android app screens** using Applitools Eyes, Appium, the Native Mobile Library (NML) and pytest.

| Folder | Platform | Sample app |
|---|---|---|
| [`ios/`](ios) | iOS Simulator | `ios/app/AccessibilityTestUIKit.app` |
| [`android/`](android) | Android emulator | `android/app/Accessibility_static_xmllayout.apk` |

Each folder works on its own: install, export the Figma frames with the Applitools Eyes Figma plugin, put the Figma values in `figma_config.py`, and run `pytest`. Start with the README in the folder for your platform.

How it works:

1. The **Applitools Eyes Figma plugin** exports each Figma frame to Eyes as a baseline.
2. The **test** opens the app with Appium, NML captures the screen, and Eyes compares it with the Figma frame. The test uses the same app name, test name (= frame name) and Baseline name as the plugin export (`set_baseline_env_name`).
