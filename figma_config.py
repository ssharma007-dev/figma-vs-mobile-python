"""
Shared by step 1 (Figma plugin export, or figma_baseline.py) and step 2 (pytest).

The Applitools Eyes Figma plugin exports every selected frame as its own Eyes test:
  - App name   = "<Figma file name> - <Figma page name>" (editable in the plugin)
  - Test name  = the frame name
  - Step name  = the frame name
  - Baseline name = shown under "Eyes configuration details" in the plugin
The device test must use the SAME app name, test name, step name and baseline
name — that is what makes Eyes compare the device screen against the Figma frame.

NML and SDK (classic Appium screenshot) captures have different geometry, so
each has its own Figma frames:
  - NML captures the full app window (status bar area included); Android full page.
  - SDK crops the status bar (≈53pt iOS / ≈54dp Android) — its frames are the same
    design shifted up by that amount. Classic Android doesn't scroll this screen,
    so Android SDK is viewport only.
"""
from appium.webdriver.common.appiumby import AppiumBy

# https://www.figma.com/design/xC9J1Z2yFx5XYc7Uglv5KE
FIGMA_FILE_KEY = "xC9J1Z2yFx5XYc7Uglv5KE"

# The plugin's "App name" field (default: "<Figma file name> - <Figma page name>").
APP_NAME = "NML Python – Figma vs Mobile (demo) - Page 1"

IOS_CHECKLIST = [AppiumBy.ACCESSIBILITY_ID, "Metric panel"]
ANDROID_CHECKLIST = [AppiumBy.ID, "com.applitools.accessibilitytest:id/tvMetricChecklist"]

PLACEHOLDER = "<paste from Figma plugin>"

# One entry per Figma frame = one Eyes test.
#   frame              — Figma frame name (the plugin's test name and step name)
#   baseline_env_name  — copy "Baseline name" from the plugin's "Eyes configuration details"
#   node_id            — only used by figma_baseline.py (no-plugin alternative)
#   fully              — False: visible screen only; True: full scrollable screen
FRAMES = {
    "nml_ios": [
        {"frame": "iOS / Main Screen", "baseline_env_name": PLACEHOLDER,
         "node_id": "1:28", "fully": False},   # 393x852
        {"frame": "iOS / Main Screen | Full", "baseline_env_name": PLACEHOLDER,
         "node_id": "3:2", "fully": True},     # 393x2056
    ],
    "nml_android": [
        {"frame": "Android / Main Screen", "baseline_env_name": PLACEHOLDER,
         "node_id": "2:2", "fully": True},     # 411x1898
    ],
    # Regions are applied with SDK captures (NML drops them — see README).
    "sdk_ios": [
        {"frame": "SDK / iOS / Viewport", "baseline_env_name": PLACEHOLDER,
         "node_id": "4:2", "fully": False, "strict_region": IOS_CHECKLIST},     # 393x799
        {"frame": "SDK / iOS / Full Page", "baseline_env_name": PLACEHOLDER,
         "node_id": "4:72", "fully": True, "strict_region": IOS_CHECKLIST},     # 393x1970
    ],
    "sdk_android": [
        {"frame": "SDK / Android / Viewport", "baseline_env_name": PLACEHOLDER,
         "node_id": "4:142", "fully": False, "strict_region": ANDROID_CHECKLIST},  # 412x847
    ],
}


def baseline_env_name(frame):
    """The plugin's Baseline name, or a fixed name when figma_baseline.py uploads the frame instead."""
    name = frame["baseline_env_name"]
    return "Figma | " + frame["frame"] if name == PLACEHOLDER else name
