import re

from playwright.sync_api import Locator, Page, expect


class DashboardPage:
    PERIODS = ("24h", "7d", "1M", "1A", "Tudo")
    METRICS = {
        "Cadastros": "1.523",
        "Transações": "2.464",
        "Taxa de Conclusão": "64%",
    }
    QUALITY_ITEMS = (
        "Conciliação financeira",
        "Cadastros completos",
        "Documentos validados",
    )

    def __init__(self, page: Page) -> None:
        self.page = page

    def expect_loaded(self) -> None:
        expect(self.page.get_by_text(re.compile("Boa tarde, Alex"))).to_be_visible()
        expect(
            self.page.get_by_text(re.compile("Atualizado|Atualização", re.IGNORECASE))
        ).to_be_visible()

    def refresh_for_period(self, period: str) -> None:
        self.page.get_by_label(re.compile("Período", re.IGNORECASE)).select_option(
            label=period
        )
        self.page.get_by_role("button", name="Atualizar", exact=True).click()

    def expect_metrics(self) -> None:
        for label, value in self.METRICS.items():
            expect(self.page.get_by_text(label, exact=True).first).to_be_visible()
            expect(self.page.get_by_text(value, exact=True).first).to_be_visible()
        expect(
            self.page.get_by_text(
                re.compile(r"Utilizadores ativos|Usuários ativos", re.IGNORECASE)
            ).first
        ).to_be_visible()
        expect(self.page.get_by_text("1.501", exact=True).first).to_be_visible()

    def use_performance_period(self, period: str) -> None:
        self.page.get_by_role("button", name=period, exact=True).click()
        expect(self.page.get_by_role("button", name=period, exact=True)).to_be_visible()

    def select_line_chart(self) -> None:
        self.page.get_by_role("button", name="Linha", exact=True).click()
        expect(self.page.get_by_role("button", name="Linha", exact=True)).to_be_visible()

    def expect_charts_and_quality(self) -> None:
        expect(self.page.get_by_text("Receita Operacional", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Frequência", exact=True)).to_be_visible()
        expect(
            self.page.get_by_text("Qualidade operacional", exact=True)
        ).to_be_visible()
        for item in self.QUALITY_ITEMS:
            expect(self.page.get_by_text(item, exact=True)).to_be_visible()
        progress_bars = self.page.get_by_role("progressbar")
        expect(progress_bars.first).to_be_visible()
        assert progress_bars.count() >= len(self.QUALITY_ITEMS), (
            "Esperadas barras de progresso para todos os indicadores de qualidade."
        )
        expect(self.page.locator("svg, canvas").first).to_be_visible()

    def navigate_calendar(self) -> None:
        expect(self.page.get_by_text("Outubro de 2026", exact=True)).to_be_visible()
        previous = self.page.get_by_role(
            "button", name=re.compile("mês anterior|mês precedente|previous month", re.I)
        )
        next_month = self.page.get_by_role(
            "button", name=re.compile("próximo mês|mês seguinte|next month", re.I)
        )
        previous.click()
        expect(self.page.get_by_text("Setembro de 2026", exact=True)).to_be_visible()
        next_month.click()
        expect(self.page.get_by_text("Outubro de 2026", exact=True)).to_be_visible()
