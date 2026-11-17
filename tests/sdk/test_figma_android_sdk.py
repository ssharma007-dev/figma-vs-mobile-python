"""Android app screen (SDK capture) vs its Figma frames."""
from figma_config import FRAMES
from figma_check import check_against_figma

FRAMES_SDK_ANDROID = FRAMES["sdk_android"]


def test_main_screen_matches_figma_android_sdk(sdk_android_driver, figma_eyes):
    check_against_figma(figma_eyes, sdk_android_driver, FRAMES_SDK_ANDROID)
