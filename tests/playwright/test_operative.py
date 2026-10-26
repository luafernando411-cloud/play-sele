import pytest
from playwright.sync_api import Page

from pages.navigation_page import NavigationPage
from pages.operative_page import OperativePage


@pytest.fixture
def operative(authenticated_page: Page) -> OperativePage:
    navigation = NavigationPage(authenticated_page)
    navigation.expand_operative()
    navigation.open_main_item("Visão geral")
    return OperativePage(authenticated_page)


def test_operational_actions_and_tabs(operative: OperativePage) -> None:
    operative.export_json()
    operative.verify_now()
    for tab in operative.TABS:
        operative.select_tab(tab)


@pytest.mark.parametrize(("tab", "resource", "status"), OperativePage.RESOURCE_STATUSES)
def test_operational_resource_statuses(
    operative: OperativePage, tab: str, resource: str, status: str
) -> None:
    operative.select_tab(tab)
    operative.expect_resource_status(resource, status)


@pytest.mark.parametrize("term", ("API Core 01", "Falhou"))
def test_operational_cross_search(operative: OperativePage, term: str) -> None:
    operative.select_tab("Consulta")
    operative.filter_and_consult(term)
    operative.expect_resource_status(
        term,
        "Operacional" if term == "API Core 01" else "Falhou",
    )


def test_export_operational_search_result(operative: OperativePage) -> None:
    operative.select_tab("Consulta")
    operative.filter_and_consult("API Core 01")
    operative.export_result()
