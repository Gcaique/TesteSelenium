# Suite de Testes Web/Mobile com Selenium + Pytest

## Visão geral
Automação funcional web e mobile (browser) usando Selenium 4 e Pytest. Suporta execução local (Chrome/Firefox) e grids remotos (LambdaTest, BrowserStack, Sauce Labs), com ajustes via CLI e um launcher visual para disparar cenários. Os testes estão em `Testes/` e `Testes_Mobile/`, organizados por contexto/região.

## Estrutura rápida
- `Testes/PROD/Default` e `Testes/PROD/Sul`: suítes web por região.
- `Testes_Mobile/`: casos para mobile.
- `helpers/`: utilitários de interação (`actions.py`, `waiters.py` etc.).
- `locators/`: mapeamento de elementos.
- `config.py`: criação de drivers locais e remotos.
- `conftest.py`: opções de CLI, fixtures base e integrações com providers.
- `run_gui.py`: interface gráfica para seleção/execução de testes.
- `pytest.ini`: opções padrão e marcadores existentes.

## Pré-requisitos
- Python 3.11+ e `pip`.
- Navegadores locais: Chrome ou Firefox (quando `--grid local`).
- Credenciais para grids conforme provedor:
  - LambdaTest: `LT_USERNAME`, `LT_ACCESS_KEY`
  - BrowserStack: `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`
  - Sauce Labs: `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`, opcional `SAUCE_REGION` (`us-west`, `us-east`, `eu-central`)
- Variáveis opcionais: `URL` (base), `USERNAME`/`PASSWORD` (login de teste) e demais chaves do seu ambiente.

## Configuração do ambiente
### Windows (PowerShell)
```pwsh
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # edite com suas chaves
```

### Linux / macOS (bash)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edite com suas chaves
```

## Como executar testes (CLI)
- Todos os testes (saída padrão): `pytest`
- Arquivo específico: `pytest Testes/PROD/Default/test_1_userDeslogado.py`
- Filtrar por substring do nome: `pytest -k "userLogado"`
- Paralelismo (requer `pytest-xdist`): `pytest -n auto`

### Flags principais do `conftest.py`
Podem ser combinadas em qualquer comando `pytest`:
- `--ambiente` `desktop|mobile` (padrão `desktop`)
- `--navegador` `chrome|firefox|edge|safari` (padrão `chrome`; em mobile iOS força `safari`)
- `--so` sistema operacional do grid (ex.: `Windows 11`, `ios`, `android`)
- `--device` nome do device para mobile (ex.: `"iPhone 14"`, `"Pixel 7"`)
- `--grid` `lt|bs|sauce|local` (padrão `bs`; `local` usa drivers instalados)
- `--base-url` URL base (usa `URL` se omitido)
- `--username` / `--password` credenciais de login
- `--timeout` timeout padrão do `WebDriverWait` (s)
- `--headless` executa browsers locais sem UI
- `--resolution` resolução desktop `LARGURAxALTURA` (ex.: `1920x1080`)

Exemplo (mobile em BrowserStack):
```bash
pytest --ambiente mobile --grid bs --so ios --navegador safari --device "iPhone 14" --base-url https://sua-url
```

## Executar testes via GUI
Com o ambiente virtual ativado:
- Windows: `.\run_gui.bat`
- Linux/macOS: `./run_gui.sh` (assegure permissão de execução: `chmod +x run_gui.sh`)

A GUI lê `Testes/` e `Testes_Mobile/`, permite selecionar arquivos, definir grid/navegador/ambiente/resolução e inicia o `pytest`. Logs e saída ficam no terminal que lançou o script.

## Dicas rápidas
- Mantenha `.env` baseado em `.env.example` para centralizar chaves.
- Para paralelismo ou filtragem por nome, use `-n auto` e `-k "<substring>"`.
- Em grids mobile, informe `--device` para evitar alocação genérica.

