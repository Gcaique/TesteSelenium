# Primeiros passos

Este passo a passo é para alguém que acabou de baixar o projeto e quer rodar os testes pela primeira vez.

## 1) O que você precisa ter instalado

- Python 3.11+.
- Git.
- Um navegador local (Chrome ou Firefox) se for rodar em `--grid local`.

Opcional:

- Credenciais de provider (LambdaTest/BrowserStack/Sauce Labs) se você for rodar em execução remota.

## 2) Baixar o projeto (clonar)

Abra o terminal no seu computador e rode:

```bash
git clone https://github.com/Gcaique/TesteSelenium.git
cd TesteSelenium
```

## 3) Preparar o ambiente Python (instalar dependências)

### Windows (PowerShell)

Crie o ambiente virtual (uma “pasta” isolada com as bibliotecas do projeto):

```pwsh
python -m venv .venv
```

Ative o ambiente virtual:

```pwsh
.\.venv\Scripts\activate
```

Instale as dependências do projeto:

```pwsh
pip install -r requirements.txt
```

### Linux / macOS (bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Configurar o arquivo .env (URLs e credenciais)

O `.env` é um arquivo onde você coloca configurações do seu ambiente (URLs e, se necessário, credenciais de execução remota).

Crie o `.env` a partir do exemplo:

Windows (PowerShell):

```pwsh
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Edite o `.env` e configure pelo menos a URL base do site:

- `URL_PROD` (ou `URL` como fallback).

Se você for usar execução remota, configure também as credenciais do provider (ver **Configuração e variáveis**).

## 5) Primeira execução (sanidade)

Existem duas formas: pelo `run_gui` (mais simples) ou pelo terminal.

### Opção A (recomendada): usar o run_gui

- Windows: execute `run_gui.bat`.
- Linux/macOS: execute `./run_gui.sh` (se necessário, `chmod +x run_gui.sh`).

Dentro do GUI:

1. Selecione um **Plano de teste** (por exemplo, Smoke).
2. Clique em **Executar**.

### Opção B: rodar pelo terminal (CLI)

Se você quiser validar via terminal, rode um teste único em modo desktop/local:

```bash
pytest -q Testes/PROD/Default/test_1_userDeslogado.py --grid local --ambiente desktop --navegador chrome
```

Se esse arquivo não existir no seu projeto (ex.: você adaptou para outro e-commerce), rode um smoke rápido:

```bash
pytest -q -m smoke Testes --grid local --ambiente desktop --navegador chrome
```

Ou rode qualquer teste individual (substitua pelo caminho de um `test_*.py` que exista):

```bash
pytest -q <caminho/do/seu/teste.py> --grid local --ambiente desktop --navegador chrome
```

## 6) Se algo der errado (checklist rápido)

- O ambiente virtual está ativado? (no Windows, você vê `(.venv)` no começo da linha do terminal).
- As dependências foram instaladas? (`pip install -r requirements.txt`).
- O `.env` existe e tem URL configurada?
- Você está tentando rodar `--grid local` sem ter Chrome/Firefox instalado?
