# Estrutura do projeto

Este documento descreve onde ficam os testes e componentes principais, e quais regras seguir para manter a suíte consistente, estável e fácil de manter.

## Pastas principais

- `Testes/`: testes web (desktop).
- `Testes_Mobile/`: testes mobile (execução em device/emulação via provider, ou execução mobile configurada via grid).
- `helpers/`: funções de interação (click), sincronização (waits) e fluxos reutilizáveis.
- `locators/`: seletores (mapeamento de elementos) centralizados. 
- `evidencias_local/`: evidências locais de falha (principalmente quando roda em `--grid local` com `--record-screen`).
- `documentacao/`: documentação em Markdown (uso e padrões do projeto).

## Organização de testes (padrão)

Os testes ficam separados por plataforma (desktop/mobile) e por variação/região (ex.: Default e Sul).

- Desktop: `Testes/PROD/Default/` e `Testes/PROD/Sul/`.
- Mobile: `Testes_Mobile/PROD/Default/` e `Testes_Mobile/PROD/Sul/`.

Regras recomendadas:

- Nome de arquivo: `test_*.py` (ex.: `test_checkout.py`).
- Nome de teste: `def test_...():` com descrição curta e objetiva.
- Use marcadores do `pytest.ini` para facilitar seleção (ex.: `smoke`, `regressao`, `mobile`, `default`, `sul`).
- Evite duplicar o mesmo fluxo em arquivos diferentes. Quando o fluxo for comum, extraia para `helpers/` e deixe o teste só com asserções e variações.

## Helpers (reuso e estabilidade)

O objetivo de `helpers/` é reduzir repetição.

Regras recomendadas:

- Prefira usar utilitários de sincronização em `helpers/waiters.py` em vez de `time.sleep`.
- Prefira interações encapsuladas em `helpers/actions.py` (ex.: cliques robustos e scroll seguro).
- Quando um fluxo for reaproveitável (login, carrinho, checkout, region switch), coloque em um helper específico (por exemplo, `helpers/checkout.py`) e reuse nos testes.

## Locators (seletores)

`locators/` centraliza os seletores usados pelos testes e helpers.

Regras recomendadas:

- Ao criar um seletor novo, adicione no arquivo correspondente em `locators/` (ou crie um novo arquivo se fizer sentido).
- Evite XPath frágil e seletor baseado em texto dinâmico.
- Reuse seletores existentes antes de criar novos, para manter consistência e reduzir manutenção.

## Evidências locais (falhas)

`evidencias_local/` é a pasta padrão para evidências geradas localmente.

Regras importantes:

- Em providers (`lt`, `bs`, `sauce`), normalmente as evidências ficam no painel do provider (vídeo/screenshot). Para evitar duplicidade, o projeto tende a não gerar evidência local nesses casos.
- Em execução local, quando `--record-screen` está habilitado, o projeto pode gerar evidência (ex.: GIF curto) no momento da falha.
- A pasta base pode ser sobrescrita com `PYTEST_ARTIFACTS_ROOT`.

## Arquivos importantes (raiz do projeto)

- `conftest.py`: opções de CLI, fixtures e regras de setup (inclui URL base e evidências em falha).
- `config.py`: criação de drivers (local e remotos) e capabilities/capacidades por provider.
- `pytest.ini`: marcadores e configurações base do pytest.
- `run_gui.py`, `run_gui.bat`, `run_gui.sh`: executor visual (seleção/configuração/execução e histórico).
- `test_plans.json`: definição de planos (ex.: Smoke/Regressão. via GUI) e paths associados.
- `.env` e `.env.example`: configuração de URLs e credenciais (não commitar `.env`).

## Boas práticas ao evoluir a estrutura

- Se adicionar novos marcadores, registre no `pytest.ini` e use de forma consistente nos testes.
- Se alterar quais testes são `smoke`/`regressao`, atualize também os planos de teste (quando aplicável).
- Se um arquivo/pasta ficar específico demais para uma região, extraia a variação para helper (ex.: `helpers/region.py`) em vez de duplicar testes.
