"""
Everything that links the Figma frames to the Android test.

The Applitools Eyes Figma plugin exports every selected frame as its own Eyes test:
  - App name      = "<Figma file name> - <Figma page name>" (editable in the plugin)
  - Test name     = the frame name
  - Step name     = the frame name
  - Baseline name = shown under "Eyes configuration details" in the plugin
The Android test uses the SAME values, so Eyes compares the app screen with the Figma frame.
"""

# The plugin's "App name" field.
APP_NAME = "NML Python – Figma vs Mobile (demo) - Page 1"

# Only used by figma_baseline.py (no-plugin alternative): https://www.figma.com/design/<file key>/...
FIGMA_FILE_KEY = "xC9J1Z2yFx5XYc7Uglv5KE"

PLACEHOLDER = "<paste from Figma plugin>"

# One entry per Figma frame = one Eyes test, per capture mode (CAPTURE=nml or CAPTURE=sdk).
#   frame              — Figma frame name (the plugin's test name and step name)
#   baseline_env_name  — "Baseline name" copied from the plugin's "Eyes configuration details"
#   node_id            — only used by figma_baseline.py (node-id=1-28 in the Figma URL → "1:28")
#   fully              — False: visible screen only; True: full scrollable screen
FRAMES = {
    # NML (Native Mobile Library inside the app) captures the full app window, status bar included.
    "nml": [
        {"frame": "Android / Main Screen", "baseline_env_name": PLACEHOLDER,
         "node_id": "2:2", "fully": True},     # 411x1898 — Android NML always captures the full scrollable screen
    ],
    # SDK (classic Appium screenshot) crops the status bar (≈54dp), so it has its own Figma frames.
    # Classic Android doesn't scroll this screen, so the frame is the visible screen only.
    "sdk": [
        {"frame": "SDK / Android / Viewport", "baseline_env_name": PLACEHOLDER,
         "node_id": "4:142", "fully": False},  # 412x847
    ],
}


def baseline_env_name(frame):
    """The plugin's Baseline name, or a fixed name when figma_baseline.py uploads the frame instead."""
    name = frame["baseline_env_name"]
    return "Figma | " + frame["frame"] if name == PLACEHOLDER else name
