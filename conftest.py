"""
Step 2 — device checkpoints compared against the Figma baselines (pytest)

  tests/nml/  NML capture (in-app library)
  tests/sdk/  classic Eyes Appium SDK capture (Appium screenshot, no NML)

ENV VARS:
  APPLITOOLS_API_KEY     — Applitools API key (required)
  APPLITOOLS_SERVER_URL  — optional; defaults to the Applitools public cloud
  APPIUM_URL             — optional; default http://127.0.0.1:4723
  MATCH_LEVEL            — LAYOUT (default) | STRICT
  Android: ANDROID_UDID (optional), AVD_NAME, PLATFORM_VERSION
  iOS:     IOS_UDID (optional), DEVICE_NAME, PLATFORM_VERSION

PREREQUISITES:
  - The Figma frames are exported with the Applitools Eyes Figma plugin and their
    Baseline names are in figma_config.py (step 1; or run figma_baseline.py)
  - A local Appium server (`appium`) and a booted emulator / Simulator
  - static_instrumented_sample_application/ copied from the main branch
"""
import os

import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from applitools.selenium import BatchInfo, ClassicRunner, Configuration, Eyes, MatchLevel

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ANDROID_APP = "static_instrumented_sample_application/android/Accessibility/Accessibility_static_xmllayout.apk"
IOS_APP = "static_instrumented_sample_application/ios/Accessibility/AccessibilityTestUIKit.app"


def app_path(relative_path):
    # Appium resolves relative app paths against its own working directory.
    path = os.path.join(PROJECT_ROOT, relative_path)
    if not os.path.exists(path):
        pytest.exit("App not found: {}\nCopy static_instrumented_sample_application/ "
                    "from the main branch first (see README).".format(path))
    return path


@pytest.fixture(scope="session")
def api_key():
    key = os.getenv("APPLITOOLS_API_KEY")
    if not key:
        pytest.exit("APPLITOOLS_API_KEY is not set")
    return key


@pytest.fixture(scope="session")
def server_url():
    return os.getenv("APPLITOOLS_SERVER_URL")


@pytest.fixture(scope="session")
def runner():
    runner = ClassicRunner()
    yield runner
    print("\n" + str(runner.get_all_test_results(False)))


def start_driver(caps, api_key, server_url, nml):
    if nml:
        # NML: inject the launch arguments that let the in-app library capture screens.
        Eyes.set_mobile_capabilities(caps, api_key, server_url)
    # Without it, Eyes captures through Appium screenshots (classic SDK).
    driver = webdriver.Remote(os.getenv("APPIUM_URL", "http://127.0.0.1:4723"),
                              options=AppiumOptions().load_capabilities(caps))
    driver.implicitly_wait(10)
    return driver


def android_caps():
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": os.getenv("AVD_NAME", "Pixel_9"),
        "appium:platformVersion": os.getenv("PLATFORM_VERSION", "16"),
        "appium:uiautomator2ServerLaunchTimeout": 90000,
        "appium:noReset": False,
        "appium:app": app_path(ANDROID_APP),
        "appium:appPackage": "com.applitools.accessibilitytest",
        "appium:appActivity": "com.applitools.accessibilitytest.MainActivity",
    }
    if os.getenv("ANDROID_UDID"):
        caps["appium:udid"] = os.environ["ANDROID_UDID"]
    return caps


def ios_caps():
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": os.getenv("DEVICE_NAME", "iPhone 16"),
        "appium:platformVersion": os.getenv("PLATFORM_VERSION", "18.0"),
        "appium:noReset": False,
        "appium:app": app_path(IOS_APP),
    }
    if os.getenv("IOS_UDID"):
        caps["appium:udid"] = os.environ["IOS_UDID"]
    return caps


def _driver(caps, api_key, server_url, nml):
    driver = start_driver(caps, api_key, server_url, nml)
    yield driver
    driver.quit()


@pytest.fixture
def nml_android_driver(api_key, server_url):
    yield from _driver(android_caps(), api_key, server_url, nml=True)


@pytest.fixture
def sdk_android_driver(api_key, server_url):
    yield from _driver(android_caps(), api_key, server_url, nml=False)


@pytest.fixture
def nml_ios_driver(api_key, server_url):
    yield from _driver(ios_caps(), api_key, server_url, nml=True)


@pytest.fixture
def sdk_ios_driver(api_key, server_url):
    yield from _driver(ios_caps(), api_key, server_url, nml=False)


@pytest.fixture
def figma_eyes(runner, api_key, server_url):
    """Returns a function that makes an Eyes instance pointed at one Figma baseline."""
    created = []

    def _make(baseline_env_name):
        config = Configuration()
        config.set_api_key(api_key)
        if server_url:
            config.set_server_url(server_url)
        config.set_batch(BatchInfo("Figma vs Device | Python"))
        # The key line: compare against the baseline the Figma plugin created.
        config.set_baseline_env_name(baseline_env_name)
        config.set_match_level(MatchLevel[os.getenv("MATCH_LEVEL", "LAYOUT").upper()])
        eyes = Eyes(runner)
        eyes.set_configuration(config)
        created.append(eyes)
        return eyes

    yield _make

    # Tests close each Eyes after its check; anything still open failed midway.
    for eyes in created:
        if eyes.is_open:
            eyes.abort()
