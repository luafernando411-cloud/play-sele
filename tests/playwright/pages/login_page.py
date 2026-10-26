from playwright.sync_api import Locator, Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def username(self) -> Locator:
        return self.page.get_by_role("textbox").nth(0)

    @property
    def password(self) -> Locator:
        return self.page.get_by_role("textbox").nth(1)

    @property
    def two_factor_code(self) -> Locator:
        return self.page.get_by_role("textbox").nth(2)

    @property
    def submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Entrar no Console")

    @property
    def request_code_button(self) -> Locator:
        return self.page.get_by_role("button", name="Solicitar Código")

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def expect_login_screen(self) -> None:
        expect(
            self.page.get_by_role("img", name="Dotal consultoria")
        ).to_be_visible()
        expect(
            self.page.get_by_text(
                "NEXO OPERATIVE · GOVERNANÇA PREVIDENCIÁRIA", exact=True
            )
        ).to_be_visible()
        expect(self.page.get_by_text("Acesso Administrativo", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Autenticação de Console", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Usuário", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Senha", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Código 2FA", exact=True)).to_be_visible()
        expect(self.username).to_be_visible()
        expect(self.password).to_be_visible()
        expect(self.two_factor_code).to_be_visible()
        expect(self.submit_button).to_be_visible()
        expect(self.submit_button).to_be_enabled()
        expect(self.request_code_button).to_be_visible()

    def login(self, username: str, password: str, two_factor_code: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.two_factor_code.fill(two_factor_code)
        self.submit_button.click()

    def request_code(self) -> None:
        self.request_code_button.click()
