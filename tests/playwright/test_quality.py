import re

from playwright.sync_api import Page, expect

from pages.navigation_page import NavigationPage
from pages.quality_page import QualityPage


def test_quality_table_and_severity_rows(authenticated_page: Page) -> None:
    NavigationPage(authenticated_page).open_main_item("Qualidade")
    quality = QualityPage(authenticated_page)
    quality.expect_table()

    critical = quality.expect_issue("CRITICAL", "Endereço", "CEP divergente")
    warning = quality.expect_issue("WARNING", "Dependente", "Documento ausente")
    ok = quality.expect_issue("OK", "CPF", "Validação em resumo")

    critical_color = critical.get_by_text("CRITICAL", exact=True).evaluate(
        "(element) => getComputedStyle(element).backgroundColor"
    )
    warning_color = warning.get_by_text("WARNING", exact=True).evaluate(
        "(element) => getComputedStyle(element).backgroundColor"
    )
    ok_color = ok.get_by_text("OK", exact=True).evaluate(
        "(element) => getComputedStyle(element).backgroundColor"
    )
    colors = {}
    for severity, color in (
        ("CRITICAL", critical_color),
        ("WARNING", warning_color),
        ("OK", ok_color),
    ):
        channels = [int(channel) for channel in re.findall(r"\d+", color)]
        assert len(channels) >= 3, f"Cor CSS inesperada para {severity}: {color}"
        red, green, blue = channels[:3]
        colors[severity] = color
        if severity == "CRITICAL":
            assert red > green and red > blue, f"CRITICAL deve ser vermelho: {color}"
        elif severity == "WARNING":
            assert red > blue and green > blue, f"WARNING deve ser amarelo: {color}"
        else:
            assert green > red and green > blue, f"OK deve ser verde: {color}"
    assert len(set(colors.values())) == 3, "Badges devem ter cores distintas."


def test_correct_first_critical_quality_issue(authenticated_page: Page) -> None:
    NavigationPage(authenticated_page).open_main_item("Qualidade")
    QualityPage(authenticated_page).correct_first_critical_issue()
