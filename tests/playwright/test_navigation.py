from playwright.sync_api import Page, expect

from pages.navigation_page import NavigationPage


def test_main_sidebar_navigation_and_instance(
    authenticated_page: Page,
) -> None:
    navigation = NavigationPage(authenticated_page)
    for name in navigation.MAIN_ITEMS:
        navigation.open_main_item(name)

    navigation.expand_operative()
    navigation.expect_instance()


def test_operative_submenu_links(authenticated_page: Page) -> None:
    navigation = NavigationPage(authenticated_page)
    navigation.expand_operative()
    for name in navigation.OPERATIVE_ITEMS:
        navigation.open_main_item(name)
