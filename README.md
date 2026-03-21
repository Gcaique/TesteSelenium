# Suite de Testes Web/Mobile com Selenium + Pytest

## Visão geral
Automação funcional web e mobile (browser) usando Selenium 4 e Pytest. O projeto suporta execução local (Chrome/Firefox) e em grids remotos (LambdaTest, BrowserStack, Sauce Labs), com ajustes de ambiente via linha de comando e um launcher visual (`run_gui.py`) para disparar cenários específicos. Os testes vivem em `Testes/` e `Testes_Mobile/`, organizados por contexto/região.

## Estrutura rápida
- `Testes/PROD/Default` e `Testes/PROD/Sul`: suítes web por região.
- `Testes_Mobile/`: casos específicos para mobile (quando existirem).
- `helpers/`: utilitários de interação (`actions.py`, `waiters.py` etc.).
- `locators/`: mapeamento de elementos.
- `config.py`: criação de drivers locais e remotos.
- `conftest.py`: opções de CLI, fixtures base e integrações com providers.
- `run_gui.py`: interface gráfica para selecionar e executar testes.
- `pytest.ini`: marcações e caminhos padrão.

## Pré-requisitos
- Python 3.11+ (recomendado) e `pip`.
- Navegadores locais: Chrome ou Firefox instalados (para grid `local`).
- Credenciais dos grids, conforme o provedor que você pretende usar:
  - LambdaTest: `LT_USERNAME`, `LT_ACCESS_KEY`
  - BrowserStack: `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`
  - Sauce Labs: `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`, opcional `SAUCE_REGION` (`us-west`, `us-east`, `eu-central`)
- Variáveis opcionais para os testes: `URL` (base do site), `USERNAME`/`PASSWORD` (login usado por fixtures), e quaisquer chaves adicionais do seu ambiente.

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

## Como executar os testes
- Todos os testes (modo padrão silencioso): `pytest`
- Um arquivo específico: `pytest Testes/PROD/Default/test_1_userDeslogado.py`
- Filtrar por substring do nome: `pytest -k "userLogado"`
- Por marcador (ver lista em `pytest.ini`): `pytest -m smoke`
- Ajustar paralelismo (se desejar, requer pytest-xdist): `pytest -n auto`

## Execução customizada (flags principais do `conftest.py`)
Use-as em qualquer comando `pytest`:
- `--ambiente` `desktop|mobile` (padrão `desktop`)
- `--navegador` `chrome|firefox|edge|safari` (padrão `chrome`; em mobile ios força `safari`)
- `--so` sistema operacional para o grid (ex.: `Windows 11`, `ios`, `android`)
- `--device` nome do device para mobile (ex.: `"iPhone 14"`, `"Pixel 7"`)
- `--grid` `lt|bs|sauce|local` (padrão `lt`; `local` usa drivers instalados)
- `--base-url` URL base (cai em `URL` do ambiente se omitido)
- `--username` / `--password` credenciais de login
- `--timeout` timeout padrão do `WebDriverWait` (segundos)
- `--headless` executa browsers locais sem UI
- `--resolution` resolução desktop no formato `LARGURAxALTURA` (ex.: `1920x1080`)

Exemplo completo:
```bash
pytest -m mobile --ambiente mobile --grid bs --so ios --navegador safari --device "iPhone 14" --base-url https://sua-url
```

## Executar testes via GUI (opcional)
Com o ambiente virtual ativado:
```bash
python run_gui.py
```
Selecione os arquivos, defina flags (ambiente, grid, navegador, resolução) e inicie a execução. O app lê automaticamente `Testes/` e `Testes_Mobile/`.

## Dicas rápidas
- Guarde suas chaves no `.env` (baseado em `.env.example`).
- Para novos marcadores, adicione-os em `pytest.ini` para visibilidade.
- Em grids móveis, informe `--device` para evitar alocação genérica.

