import os
from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect, sync_playwright

from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def base_url() -> str:
    value = os.getenv(
        "APP_BASE_URL", "https://codespaces-react-main-l56h.onrender.com/"
    )
    return value.rstrip("/")


@pytest.fixture(scope="session")
def credentials() -> dict[str, str] | None:
    required = {
        "username": "E2E_USERNAME",
        "password": "E2E_PASSWORD",
        "two_factor_code": "E2E_2FA_CODE",
    }
    missing = [env_name for env_name in required.values() if not os.getenv(env_name)]
    if missing:
        if os.getenv("CI", "").lower() == "true":
            pytest.fail(
                "Defina as variáveis de autenticação para CI: "
                + ", ".join(missing)
            )
        return None
    return {key: os.environ[env_name] for key, env_name in required.items()}


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    with sync_playwright() as playwright:
        headless = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() != "false"
        instance = playwright.chromium.launch(headless=headless)
        yield instance
        instance.close()


@pytest.fixture
def page(browser: Browser) -> Iterator[Page]:
    context: BrowserContext = browser.new_context(
        accept_downloads=True,
        viewport={"width": 1440, "height": 1000},
    )
    current_page = context.new_page()
    current_page.set_default_timeout(10_000)
    yield current_page
    context.close()


@pytest.fixture
def authenticated_page(
    page: Page, base_url: str, credentials: dict[str, str] | None
) -> Page:
    login = LoginPage(page)
    login.open(base_url)
    if credentials:
        login.login(
            username=credentials["username"],
            password=credentials["password"],
            two_factor_code=credentials["two_factor_code"],
        )
    else:
        login.submit_button.click()
    expect(page.get_by_text("Painel", exact=True).first).to_be_visible()
    return page
