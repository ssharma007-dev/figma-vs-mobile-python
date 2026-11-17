from applitools.selenium import Target

from figma_config import APP_NAME, baseline_env_name


def check_against_figma(figma_eyes, driver, frames):
    """One Eyes test per Figma frame, named like the plugin export: test name = step name = frame name."""
    for frame in frames:
        eyes = figma_eyes(baseline_env_name(frame))
        eyes.open(driver, APP_NAME, frame["frame"])
        target = Target.window().fully(frame["fully"])
        if frame.get("strict_region"):
            # Layout for the screen as a whole, pixel-exact for the content that must match.
            target = target.strict(frame["strict_region"])
        eyes.check(frame["frame"], target)
        results = eyes.close(raise_ex=False)
        print("\n{} → {} ({} mismatches) {}".format(
            frame["frame"], results.status, results.mismatches, results.url))
