"""Android app screen (SDK capture) vs its Figma frames."""
from figma_config import APP_NAME, DESIGNS
from figma_check import check_against_figma

DESIGN = DESIGNS["sdk_android"]


def test_main_screen_matches_figma_android_sdk(sdk_android_driver, figma_eyes):
    check_against_figma(figma_eyes(DESIGN), sdk_android_driver, APP_NAME, DESIGN)
