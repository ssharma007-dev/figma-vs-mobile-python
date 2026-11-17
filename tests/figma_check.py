from applitools.selenium import Target


def check_against_figma(eyes, driver, app_name, design):
    """One Eyes test per design; one checkpoint per Figma frame, in the same order as the upload."""
    eyes.open(driver, app_name, design["test_name"])
    for step in design["steps"]:
        target = Target.window().fully(step["fully"])
        if design.get("strict_region"):
            # Layout for the screen as a whole, pixel-exact for the content that must match.
            target = target.strict(design["strict_region"])
        eyes.check(step["name"], target)
