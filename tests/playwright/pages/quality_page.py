from playwright.sync_api import Locator, Page, expect


class QualityPage:
    EXPECTED_COLUMNS = (
        "Origem",
        "Segurado",
        "Detalhe",
        "Severidade",
        "Status",
        "Ação",
    )

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def table(self) -> Locator:
        return self.page.get_by_role("table").filter(
            has=self.page.get_by_role("columnheader", name="Severidade")
        ).first

    def expect_table(self) -> None:
        expect(self.table).to_be_visible()
        for column in self.EXPECTED_COLUMNS:
            expect(
                self.table.get_by_role("columnheader", name=column, exact=True)
            ).to_be_visible()

    def row_for(self, *terms: str) -> Locator:
        row = self.table.get_by_role("row").filter(has_text=terms[0])
        for term in terms[1:]:
            row = row.filter(has_text=term)
        return row.first

    def expect_issue(self, severity: str, *terms: str) -> Locator:
        row = self.row_for(*terms)
        expect(row).to_be_visible()
        expect(row.get_by_text(severity, exact=True)).to_be_visible()
        expect(row.get_by_role("button", name="Corrigir", exact=True)).to_be_visible()
        return row

    def correct_first_critical_issue(self) -> None:
        row = self.expect_issue("CRITICAL", "Endereço", "CEP divergente")
        original_url = self.page.url
        row.get_by_role("button", name="Corrigir", exact=True).click()

        dialog = self.page.get_by_role("dialog")
        try:
            expect(dialog).to_be_visible(timeout=3_000)
            return
        except AssertionError:
            pass

        self.page.wait_for_timeout(500)
        assert self.page.url != original_url, (
            "A ação Corrigir não abriu um diálogo nem redirecionou para a correção."
        )
