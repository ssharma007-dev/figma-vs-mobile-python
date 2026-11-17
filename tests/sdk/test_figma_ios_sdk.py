"""iOS app screen (SDK capture) vs its Figma frames."""
from figma_config import FRAMES
from figma_check import check_against_figma

FRAMES_SDK_IOS = FRAMES["sdk_ios"]


def test_main_screen_matches_figma_ios_sdk(sdk_ios_driver, figma_eyes):
    check_against_figma(figma_eyes, sdk_ios_driver, FRAMES_SDK_IOS)
