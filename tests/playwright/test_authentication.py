from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_screen(page: Page, base_url: str) -> None:
    login = LoginPage(page)
    login.open(base_url)
    login.expect_login_screen()


def test_login_successful_authentication(
    page: Page, base_url: str, credentials: dict[str, str] | None
) -> None:
    login = LoginPage(page)
    login.open(base_url)
    login.expect_login_screen()
    if credentials:
        login.login(
            username=credentials["username"],
            password=credentials["password"],
            two_factor_code=credentials["two_factor_code"],
        )
    else:
        login.submit_button.click()

    expect(page.get_by_text("Painel", exact=True).first).to_be_visible()
    expect(page.get_by_text("SYSADMIN · São Paulo", exact=True)).to_be_visible()


def test_request_two_factor_code_button_is_available(page: Page, base_url: str) -> None:
    login = LoginPage(page)
    login.open(base_url)
    login.expect_login_screen()
