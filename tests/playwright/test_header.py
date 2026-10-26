from playwright.sync_api import Page

from pages.header_page import HeaderPage


def test_header_status_notifications_actions_and_profile(
    authenticated_page: Page,
) -> None:
    header = HeaderPage(authenticated_page)
    header.expect_live_status()
    header.notification_badge()
    header.expect_top_actions()
    header.expect_profile()
