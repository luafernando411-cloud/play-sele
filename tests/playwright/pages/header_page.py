import re

from playwright.sync_api import Locator, Page, expect


class HeaderPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_live_status(self) -> None:
        status = self.page.get_by_text("Ao vivo", exact=True)
        expect(status).to_be_visible()
        green_indicator = self.page.locator(
            "[data-testid='live-indicator'], .live-indicator, .status-dot"
        ).first
        expect(green_indicator).to_be_visible()
        color = green_indicator.evaluate(
            "(element) => getComputedStyle(element).backgroundColor"
        )
        red, green, blue = (
            int(channel)
            for channel in re.findall(r"\d+", color)[:3]
        )
        assert green > red and green > blue, (
            f"O indicador Ao vivo deve ser verde; cor encontrada: {color}"
        )

    def notification_badge(self) -> Locator:
        notification_button = self.page.get_by_role(
            "button", name=re.compile("notificações|notifications", re.IGNORECASE)
        )
        expect(notification_button).to_be_visible()
        badge = notification_button.get_by_text("1", exact=True)
        expect(badge).to_be_visible()
        return badge

    def expect_top_actions(self) -> None:
        expect(
            self.page.get_by_role(
                "button",
                name=re.compile(r"pesquisa|buscar|search|atalho|shortcut", re.I),
            ).first
        ).to_be_visible()
        expect(
            self.page.get_by_role(
                "button",
                name=re.compile(r"configurações|configuração|settings", re.I),
            ).first
        ).to_be_visible()

    def expect_profile(self) -> None:
        expect(
            self.page.get_by_text("SYSADMIN · São Paulo", exact=True)
        ).to_be_visible()
