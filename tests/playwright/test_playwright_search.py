from urllib.parse import urlencode

from playwright.sync_api import Page, expect


def test_search_with_playwright(page: Page) -> None:
    query = "Python automation testing"
    url = f"https://en.wikipedia.org/w/index.php?{urlencode({'search': query})}"
    page.goto(url, wait_until="domcontentloaded", timeout=30_000)
    result = page.locator(".mw-search-result-heading a").first
    expect(result).to_be_visible(timeout=20_000)
    expect(result).not_to_be_empty()
