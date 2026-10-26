import pytest
from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.navigation_page import NavigationPage


@pytest.fixture
def dashboard(authenticated_page: Page) -> DashboardPage:
    NavigationPage(authenticated_page).open_main_item("Painel")
    dashboard = DashboardPage(authenticated_page)
    dashboard.expect_loaded()
    return dashboard


def test_dashboard_period_and_metrics(dashboard: DashboardPage) -> None:
    dashboard.refresh_for_period("Este mês")
    dashboard.expect_metrics()


def test_dashboard_charts_operational_quality_and_calendar(
    dashboard: DashboardPage,
) -> None:
    dashboard.expect_charts_and_quality()
    for period in dashboard.PERIODS:
        dashboard.use_performance_period(period)
    dashboard.select_line_chart()
    dashboard.navigate_calendar()
