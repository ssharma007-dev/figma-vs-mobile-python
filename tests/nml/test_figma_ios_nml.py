"""iOS app screen (NML capture) vs its Figma frames."""
from figma_config import APP_NAME, DESIGNS
from figma_check import check_against_figma

DESIGN = DESIGNS["nml_ios"]


def test_main_screen_matches_figma_ios_nml(nml_ios_driver, figma_eyes):
    check_against_figma(figma_eyes(DESIGN), nml_ios_driver, APP_NAME, DESIGN)
