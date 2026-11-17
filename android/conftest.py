"""
Appium driver (NML or classic SDK capture), and Eyes pointed at the Figma baseline.

ENV VARS:
  APPLITOOLS_API_KEY     — Applitools API key (required)
  APPLITOOLS_SERVER_URL  — optional; defaults to the Applitools public cloud
  CAPTURE                — nml (default): NML library inside the app | sdk: classic Appium screenshot
  APPIUM_URL             — optional; default http://127.0.0.1:4723
  MATCH_LEVEL            — LAYOUT (default) | STRICT
  AVD_NAME, PLATFORM_VERSION — emulator to use (default Pixel_9, 16)
  ANDROID_UDID           — optional; a specific emulator or device (see `adb devices`)
  APP_PATH               — optional; your own app instead of the sample in app/
"""
import os

import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from applitools.selenium import BatchInfo, ClassicRunner, Configuration, Eyes, MatchLevel

CAPTURE = os.getenv("CAPTURE", "nml").lower()
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_APP = os.path.join(HERE, "app/Accessibility_static_xmllayout.apk")


def app_path():
    # Appium resolves relative app paths against its own working directory, so pass an absolute path.
    path = os.path.abspath(os.getenv("APP_PATH", SAMPLE_APP))
    if not os.path.exists(path):
        pytest.exit("App not found: " + path)
    return path


def capabilities():
    caps = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": os.getenv("AVD_NAME", "Pixel_9"),
        "appium:platformVersion": os.getenv("PLATFORM_VERSION", "16"),
        "appium:uiautomator2ServerLaunchTimeout": 90000,
        "appium:noReset": False,
        "appium:app": app_path(),
        "appium:appPackage": "com.applitools.accessibilitytest",
        "appium:appActivity": "com.applitools.accessibilitytest.MainActivity",
    }
    if os.getenv("ANDROID_UDID"):
        caps["appium:udid"] = os.environ["ANDROID_UDID"]
    return caps


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


@pytest.fixture
def driver(api_key, server_url):
    caps = capabilities()
    if CAPTURE == "nml":
        # NML: adds the launch arguments that let the Applitools library inside the app capture the screen.
        Eyes.set_mobile_capabilities(caps, api_key, server_url)
    # Without it, Eyes captures through Appium screenshots (classic SDK).
    driver = webdriver.Remote(os.getenv("APPIUM_URL", "http://127.0.0.1:4723"),
                              options=AppiumOptions().load_capabilities(caps))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def figma_eyes(runner, api_key, server_url):
    """Returns a function that makes an Eyes instance pointed at one Figma baseline."""
    created = []

    def _make(baseline_env_name):
        config = Configuration()
        config.set_api_key(api_key)
        if server_url:
            config.set_server_url(server_url)
        config.set_batch(BatchInfo("Figma vs Android | Python | " + CAPTURE.upper()))
        # The key line: compare against the baseline the Figma plugin created.
        config.set_baseline_env_name(baseline_env_name)
        config.set_match_level(MatchLevel[os.getenv("MATCH_LEVEL", "LAYOUT").upper()])
        eyes = Eyes(runner)
        eyes.set_configuration(config)
        created.append(eyes)
        return eyes

    yield _make

    # Each check closes its Eyes; anything still open failed midway.
    for eyes in created:
        if eyes.is_open:
            eyes.abort()
