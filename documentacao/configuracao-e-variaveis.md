# Configuração e variáveis

## .env e URLs de ambiente

O projeto usa `.env` para centralizar configurações. As URLs são resolvidas por `--target-env`:

- `prod`: `URL`
- `stg1`: `URL_STG1`
- `stg2`: `URL_STG2`
- `outro`: use `--base-url` (ou a URL custom do GUI)

Recomendação:

- Mantenha `.env` fora do controle de versão.
- Deixe `.env.example` sempre atualizado com as chaves esperadas.

## Credenciais de grids remotos

Configure as variáveis conforme o provider:

- LambdaTest: `LT_USERNAME`, `LT_ACCESS_KEY`
- BrowserStack: `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`
- Sauce Labs: `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`

## Drivers locais

Para `--grid local`, o projeto usa `webdriver-manager` para baixar/gerenciar drivers quando necessário.

## Evidências locais (falhas)

Este projeto gera evidências locais somente quando ocorre falha e somente em execução local (para grids remotos, os próprios providers costumam fornecer vídeo/screenshot).

O que é gerado (local):

- Um GIF curto para ajudar a visualizar o estado da tela no momento da falha.

Regras importantes:

- As evidências só são geradas se a execução estiver com `--record-screen` habilitado (no GUI, checkbox **Salvar evidência**).
- Em providers (`lt`, `bs`, `sauce`), o projeto não gera evidência local para evitar duplicidade e overhead.
- As evidências são salvas por data em uma pasta `DD-MM-AAAA`, usando um nome baseado no teste (sanitizado).

Onde fica salvo:

- Por padrão, em `evidencias_local/`.
- Você pode sobrescrever a pasta base com a variável de ambiente `PYTEST_ARTIFACTS_ROOT`.

O que é `PYTEST_ARTIFACTS_ROOT`:

- É uma variável de ambiente lida pelo pytest para definir a pasta raiz onde as evidências locais serão gravadas.
- O `run_gui` define automaticamente `PYTEST_ARTIFACTS_ROOT` apontando para `evidencias_local/` durante a execução.
- Se você não definir essa variável, o padrão do projeto também é `evidencias_local/` (na raiz do repositório).

## Timeouts e performance

- `--timeout` controla o timeout padrão do `WebDriverWait`.
- Em caso de lentidão, prefira revisar a estratégia de waits nos `helpers/` antes de aumentar timeouts globalmente.
