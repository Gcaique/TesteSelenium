# Executando via CLI (terminal)

## Comandos rápidos (recomendados)

- Smoke web:

```bash
pytest -q -m smoke Testes
```

- Regressão web:

```bash
pytest -q -m regressao Testes
```

- Smoke mobile:

```bash
pytest -q -m "mobile and smoke" Testes_Mobile
```

- Regressão mobile:

```bash
pytest -q -m "mobile and regressao" Testes_Mobile
```

- Um arquivo específico:

```bash
pytest -q Testes/PROD/Default/test_1_userDeslogado.py
```

- Filtrar por parte do nome (substring):

```bash
pytest -q -k "checkout"
```

- Paralelismo (xdist):

```bash
pytest -q -n auto
```

## Smoke vs Regressão

Os marcadores são definidos no `pytest.ini`.

- `smoke`: subconjunto rápido, para sanity/PR e diagnóstico inicial.
- `regressao`: conjunto amplo, para validação completa (idealmente todo teste entra aqui, e alguns entram em `smoke`).

Recomendação de uso:

- Rode `smoke` primeiro quando estiver ajustando ambiente/infra/seletores.
- Rode `regressao` quando quiser validar cobertura completa (ou antes de releases).

## Marcadores (markers)

Exemplos comuns:

- `smoke`: suite rapida.
- `regressao`: suite ampla.
- `mobile`: testes mobile.
- `default` / `sul`: variação/região.
- `cart`, `checkout`, `dashboard`, etc.: por área.

Exemplos:

```bash
pytest -q -m "smoke and default" Testes
pytest -q -m "regressao and sul" Testes
pytest -q -m "mobile and smoke and sul" Testes_Mobile
```

## Flags de execução (principais)

As opções são definidas no `conftest.py` e podem ser combinadas no mesmo comando `pytest`.

### O que cada opção faz

- `--ambiente desktop|mobile`: seleciona o tipo de execução.
  - `desktop`: testes web (normalmente em `Testes/`).
  - `mobile`: testes mobile (normalmente em `Testes_Mobile/`) e habilita lógica de device/SO.
- `--grid local|lt|bs|sauce`: define onde o WebDriver será criado.
  - `local`: roda na sua máquina (Chrome/Firefox locais).
  - `lt` (LambdaTest), `bs` (BrowserStack), `sauce` (Sauce Labs): roda em grid remoto (requer credenciais no `.env`).
- `--navegador chrome|firefox|edge|safari`: navegador alvo.
  - Em `local`, o suporte principal é `chrome` e `firefox`.
  - Em grid remoto, pode haver variações por provider e por `--so`.
- `--so <valor>`: sistema operacional/plataforma para o provider.
  - Desktop: ex.: `Windows 11`.
  - Mobile: `Android` ou `iOS` (isso influencia navegador e tipo de sessão).
- `--device "<nome>"`: nome do dispositivo (principalmente para `--ambiente mobile`).
  - Exemplos: `"iPhone 14"`, `"Pixel 7"`.
  - Dica: nomes precisam bater com os do provider.
- `--target-env prod|stg1|stg2|outro`: escolhe qual URL usar (mapeada via `.env`).
  - `prod|stg1|stg2`: resolve a URL pelo `.env`.
  - `outro`: use junto com `--base-url`.
- `--base-url <url>`: sobrescreve a URL do ambiente.
  - Útil para apontar para outro e-commerce sem mexer no `.env`.
- `--timeout <segundos>`: timeout padrão usado nos `WebDriverWait` do projeto.
  - Use para ambientes mais lentos; evite aumentar por padrão (prefira ajustar sincronização com helpers).
- `--resolution LARGURAxALTURA`: resolução/viewport do desktop.
  - Exemplos: `1920x1080`, `1366x768`.
- `--headless`: roda o navegador sem interface (somente para `--grid local`).
  - Bom para rodar em background/CI; em grids remotos normalmente não se aplica.
- `--build-name "<nome>"`: nome lógico da execução.
  - Ajuda a agrupar execuções no provider e no histórico do `run_gui`.
- `--record-screen`: habilita captura de evidências adicionais.
  - Em grids remotos, pode habilitar vídeo/screenshots no provider (dependendo de como o driver é criado).
  - Em execução local, a evidência costuma ficar em `evidencias_local/` quando há falha.

### Exemplos curtos

Desktop local (rápido para depurar):

```bash
pytest -q -m smoke Testes --grid local --ambiente desktop --navegador chrome
```

Mobile iOS em cloud (exemplo):

```bash
pytest -q -m "mobile and smoke" Testes_Mobile --grid bs --ambiente mobile --so iOS --device "iPhone 14" --navegador safari --build-name "smoke-ios"
```

## Exemplos completos

Desktop local, headless:

```bash
pytest -q -m smoke Testes --grid local --ambiente desktop --navegador chrome --headless --resolution 1920x1080
```

Mobile em cloud (exemplo iOS):

```bash
pytest -q -m "mobile and smoke" Testes_Mobile --grid bs --ambiente mobile --so iOS --device "iPhone 14" --navegador safari
```

## Dica de diagnostico

Quando um teste falhar:

1. Rode o mesmo teste isolado (um único arquivo) para reduzir ruído.
2. Rode com `--grid local` para diferenciar falha de provider vs falha do teste.
3. Verifique evidências em `evidencias_local/` (quando aplicável) e logs no terminal/GUI.
