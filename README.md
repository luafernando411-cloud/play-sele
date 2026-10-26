# Testes automatizados com Selenium e Playwright

Ambiente Python para executar testes de navegador no GitHub Codespaces. O contêiner instala Chromium e ChromeDriver para Selenium; o comando de criação do Codespace instala as dependências Python e o Chromium do Playwright.

## 1. Preparar o Codespace

1. Abra este repositório em um Codespace.
2. Se o Codespace já estava aberto antes da inclusão de `.devcontainer`, execute **Codespaces: Rebuild Container** na paleta de comandos do VS Code.
3. Aguarde o comando de criação terminar. Ele instala as dependências de `requirements.txt` e os navegadores/dependências de sistema do Playwright.

O arquivo `.devcontainer/Dockerfile` instala Chromium e ChromeDriver para o Selenium. O arquivo `.devcontainer/devcontainer.json` automatiza a instalação das bibliotecas Python e do navegador do Playwright.

## 2. Estrutura do projeto

```text
.
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── tests/
│   ├── playwright/
│   │   ├── pages/
│   │   ├── conftest.py
│   │   └── test_*.py
│   └── selenium/
│       └── test_selenium_search.py
├── requirements.txt
├── pytest.ini
└── README.md
```

`pandas` também está incluído em `requirements.txt` para uso em utilitários e análise dos dados dos testes.

## 3. Executar os testes

No terminal integrado do Codespaces, a partir da raiz do projeto:

```bash
# Executar os dois testes
python -m pytest -v

# Executar apenas o teste Selenium
python -m pytest -v tests/selenium/test_selenium_search.py

# Executar a suíte E2E Playwright
python -m pytest -v tests/playwright
```

Também é possível executar cada script diretamente:

```bash
python tests/selenium/test_selenium_search.py
python -m pytest -v tests/playwright
```

## Suíte E2E Dotal / Nexo Operative

Os testes Playwright usam Page Object Model em `tests/playwright/pages/` e Chromium headless. A URL informada já é o padrão. Para autenticar e executar os cenários protegidos, configure credenciais de teste no terminal; não grave segredos no repositório:

```bash
export APP_BASE_URL="https://seu-ambiente.example/login"
export E2E_USERNAME="sysadmin@rpps.sp.gov.br"
export E2E_PASSWORD="sua-senha-de-teste"
export E2E_2FA_CODE="482197"

python -m pytest -v tests/playwright
```

Use somente uma conta de teste e um ambiente autorizado. O teste inicial verifica que **Solicitar Código** está disponível, sem acioná-lo, pois isso pode enviar uma mensagem real. Sem credenciais, os testes que exigem login são ignorados e os testes da tela de login continuam sendo executados. Ajuste os seletores dos Page Objects caso os rótulos acessíveis, roles ou estrutura das telas mudem.

### Executar automaticamente no GitHub Actions

O workflow `.github/workflows/playwright.yml` executa os E2E em push para `main`/`master` ou manualmente pela aba **Actions**. Cadastre os seguintes repository secrets em **Settings → Secrets and variables → Actions**:

- `APP_BASE_URL`: URL da tela de login do ambiente de teste.
- `E2E_USERNAME`: utilizador da conta de teste.
- `E2E_PASSWORD`: senha da conta de teste.
- `E2E_2FA_CODE`: código 2FA exigido pelo fluxo.

O workflow instala as dependências e o Chromium, executa `tests/playwright` em headless e publica o relatório JUnit como artifact. Códigos 2FA temporários podem expirar antes da execução; para CI confiável, use um ambiente de teste com mecanismo de autenticação apropriado para automação, sem desabilitar a segurança da produção.

Os testes Selenium fazem uma busca de exemplo na Wikipédia em inglês. É necessário que o Codespace tenha acesso à internet. Se estiver configurando o ambiente fora do Codespaces, instale as dependências com `python -m pip install -r requirements.txt`, instale o navegador do Playwright com `python -m playwright install --with-deps chromium` e disponibilize Chromium e ChromeDriver para o Selenium.
