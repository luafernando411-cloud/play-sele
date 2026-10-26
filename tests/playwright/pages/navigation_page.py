import re

from playwright.sync_api import Locator, Page, expect


class NavigationPage:
    MAIN_ITEMS = (
        "Painel",
        "Análises",
        "Cadastros",
        "Integrações",
        "Qualidade",
        "Compliance",
    )
    OPERATIVE_ITEMS = (
        "Visão geral",
        "Servidores",
        "Banco de dados",
        "Pendentes",
        "Consulta",
    )

    def __init__(self, page: Page) -> None:
        self.page = page

    def item(self, name: str) -> Locator:
        return self.page.get_by_role("link", name=name, exact=True).first

    @property
    def operative_toggle(self) -> Locator:
        return self.page.get_by_role(
            "button", name=re.compile("Nexo Operative", re.IGNORECASE)
        ).first

    def open_main_item(self, name: str) -> None:
        link = self.item(name)
        previous_url = self.page.url
        link.click()
        expect(link).to_be_visible()
        if self.page.url == previous_url:
            expect(link).to_have_attribute("aria-current", "page")

    def expand_operative(self) -> None:
        if self.operative_toggle.count():
            self.operative_toggle.click()
        else:
            self.page.get_by_text("Nexo Operative", exact=True).first.click()
        for name in self.OPERATIVE_ITEMS:
            expect(self.item(name)).to_be_visible()

    def expect_instance(self) -> None:
        expect(
            self.page.get_by_text("INSTANCE: SP-RPPS - PROD", exact=True)
        ).to_be_visible()
