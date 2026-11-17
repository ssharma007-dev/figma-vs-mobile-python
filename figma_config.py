"""
Shared by step 1 (figma_baseline.py) and step 2 (pytest).

The Figma upload and the device test must use the SAME app name, test name,
step names (in the same order) and baseline_env_name — that is what makes Eyes
compare the device screen against the Figma design.

NML and SDK (classic Appium screenshot) captures have different geometry, so
each has its own Figma frames and its own baseline:
  - NML captures the full app window (status bar area included); Android full page.
  - SDK crops the status bar (≈53pt iOS / ≈54dp Android) — its frames are the same
    design shifted up by that amount. Classic Android doesn't scroll this screen,
    so Android SDK is viewport only.
"""
from appium.webdriver.common.appiumby import AppiumBy

# https://www.figma.com/design/xC9J1Z2yFx5XYc7Uglv5KE
FIGMA_FILE_KEY = "xC9J1Z2yFx5XYc7Uglv5KE"

APP_NAME = "Accessibility App | Figma vs Device"

IOS_CHECKLIST = [AppiumBy.ACCESSIBILITY_ID, "Metric panel"]
ANDROID_CHECKLIST = [AppiumBy.ID, "com.applitools.accessibilitytest:id/tvMetricChecklist"]

DESIGNS = {
    "nml_ios": {
        "test_name": "Main Screen | iOS | NML",
        "baseline_env_name": "Figma | iOS | NML",
        "steps": [
            {"name": "Main Screen | Viewport", "node_id": "1:28", "fully": False},  # 393x852
            {"name": "Main Screen | Full Page", "node_id": "3:2", "fully": True},   # 393x2056
        ],
    },
    "nml_android": {
        "test_name": "Main Screen | Android | NML",
        "baseline_env_name": "Figma | Android | NML",
        "steps": [
            {"name": "Main Screen | Full Page", "node_id": "2:2", "fully": True},   # 411x1898
        ],
    },
    "sdk_ios": {
        "test_name": "Main Screen | iOS | SDK",
        "baseline_env_name": "Figma | iOS | SDK",
        # Regions are applied with SDK captures (NML drops them — see README).
        "strict_region": IOS_CHECKLIST,
        "steps": [
            {"name": "Main Screen | Viewport", "node_id": "4:2", "fully": False},   # 393x799
            {"name": "Main Screen | Full Page", "node_id": "4:72", "fully": True},  # 393x1970
        ],
    },
    "sdk_android": {
        "test_name": "Main Screen | Android | SDK",
        "baseline_env_name": "Figma | Android | SDK",
        "strict_region": ANDROID_CHECKLIST,
        "steps": [
            {"name": "Main Screen | Viewport", "node_id": "4:142", "fully": False},  # 412x847
        ],
    },
}
