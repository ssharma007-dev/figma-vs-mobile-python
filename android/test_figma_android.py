"""Android app screen (NML or SDK capture) vs its Figma frames."""
from applitools.selenium import Target

from conftest import CAPTURE
from figma_config import APP_NAME, FRAMES, baseline_env_name


def test_app_matches_figma(driver, figma_eyes):
    # One Eyes test per Figma frame, named like the plugin export (test name = frame name).
    for frame in FRAMES[CAPTURE]:
        eyes = figma_eyes(baseline_env_name(frame))
        eyes.open(driver, APP_NAME, frame["frame"])
        # iOS NML saves each screenshot to a file named after the step, so "/" in a frame name breaks it.
        # Eyes pairs steps by order, so the step name doesn't have to match the plugin's exactly.
        eyes.check(frame["frame"].replace("/", "-"), Target.window().fully(frame["fully"]))
        results = eyes.close(raise_ex=False)
        print("\n{} → {} ({} mismatches) {}".format(
            frame["frame"], results.status, results.mismatches, results.url))
