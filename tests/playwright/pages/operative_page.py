import re

from playwright.sync_api import Locator, Page, expect


class OperativePage:
    TABS = ("Visão geral", "Servidores", "Banco de dados", "Pendentes", "Consulta")
    RESOURCE_STATUSES = (
        ("Servidores", "API Core 01", "Operacional"),
        ("Servidores", "Worker Jobs 02", "Atenção"),
        ("Servidores", "Motor de relatórios", "Operacional"),
        ("Banco de dados", "nexo_prod", "Operacional"),
        ("Banco de dados", "events_queue", "Operacional"),
        ("Pendentes", "Aprovar lote de recadastramento", "Pendente"),
        ("Pendentes", "Reprocessar sincronização CNIS", "Pendente"),
        ("Pendentes", "Validar divergência da folha", "Falhou"),
        ("Pendentes", "Atualizar índice atuarial", "Concluído"),
    )

    def __init__(self, page: Page) -> None:
        self.page = page

    def select_tab(self, name: str) -> None:
        self.page.get_by_role("tab", name=name, exact=True).click()
        expect(self.page.get_by_role("tab", name=name, exact=True)).to_have_attribute(
            "aria-selected", "true"
        )

    def export_json(self) -> None:
        with self.page.expect_download():
            self.page.get_by_role("button", name="Exportar JSON", exact=True).click()

    def verify_now(self) -> None:
        button = self.page.get_by_role("button", name="Verificar agora", exact=True)
        expect(button).to_be_enabled()
        button.click()

    def filter_and_consult(self, term: str) -> None:
        search = self.page.get_by_placeholder(
            "Filtrar por nome, status ou origem", exact=True
        )
        search.fill(term)
        self.page.get_by_role("button", name="Consultar", exact=True).click()

    def expect_resource_status(self, resource: str, status: str) -> None:
        row = self.page.get_by_role("row").filter(has_text=resource).first
        expect(row).to_be_visible()
        expect(row.get_by_text(status, exact=True)).to_be_visible()

    def export_result(self) -> None:
        button = self.page.get_by_role(
            "button", name=re.compile("Exportar resultado", re.IGNORECASE)
        )
        with self.page.expect_download():
            button.click()
