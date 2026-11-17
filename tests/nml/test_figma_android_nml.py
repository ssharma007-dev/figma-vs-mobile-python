"""Android app screen (NML capture) vs its Figma frames."""
from figma_config import FRAMES
from figma_check import check_against_figma

FRAMES_NML_ANDROID = FRAMES["nml_android"]


def test_main_screen_matches_figma_android_nml(nml_android_driver, figma_eyes):
    check_against_figma(figma_eyes, nml_android_driver, FRAMES_NML_ANDROID)
