"""iOS app screen (NML capture) vs its Figma frames."""
from figma_config import FRAMES
from figma_check import check_against_figma

FRAMES_NML_IOS = FRAMES["nml_ios"]


def test_main_screen_matches_figma_ios_nml(nml_ios_driver, figma_eyes):
    check_against_figma(figma_eyes, nml_ios_driver, FRAMES_NML_IOS)
