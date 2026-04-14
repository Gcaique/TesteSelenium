# Solução de problemas e evidências

Este documento ajuda a identificar problemas comuns na execução dos testes e onde encontrar evidências quando algo falha.

## Problemas comuns

### URL não definida

Sintoma:

- O teste falha logo no início informando que a URL não foi encontrada/definida.

O que verificar:

- O arquivo `.env` tem `URL` configurado?
- Você está usando o `--target-env` correto (`prod|stg1|stg2|outro`)?
- Se estiver usando `--target-env outro`, você informou `--base-url` (ou a URL custom no GUI)?

### Credenciais do grid (provider) ausentes

Sintoma:

- Erro ao criar driver remoto (não consegue abrir sessão no provider).

O que verificar:

- As credenciais do provider estão no `.env`?
  - LambdaTest: `LT_USERNAME`, `LT_ACCESS_KEY`
  - BrowserStack: `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`
  - Sauce Labs: `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`
- O `.env` está sendo carregado (o projeto usa `python-dotenv`)?

### Dispositivo não encontrado (Mobile)

Sintoma:

- O provider recusa a sessão porque o nome do device não é reconhecido.

O que verificar:

- O nome do device bate exatamente com o esperado pelo provider (nomes são sensíveis).
- Se possível, selecione o device pela lista do `run_gui` para evitar erro de digitação.

### Flakiness (falha intermitente)

Sintoma:

- O teste às vezes passa e às vezes falha, sem mudança no código.

Abordagem recomendada:

1. Garanta sincronização usando `helpers/waiters.py` (`visible`, `clickable`).
2. Use interações robustas em `helpers/actions.py` (`safe_click_loc`, retries), em vez de duplicar retry no teste.
3. Evite `time.sleep` como solução padrão (além de deixar mais lento, pode mascarar o problema).

### Headless e grid

Pontos importantes:

- Headless é relevante principalmente em `--grid local`.
- No `run_gui`, marcar headless sem plataforma definida tende a forçar `local` para evitar combinações inválidas.

## Onde encontrar evidências

### Execução local

- Pasta padrão: `evidencias_local/` (ou o caminho definido por `PYTEST_ARTIFACTS_ROOT`).
- Normalmente as evidências aparecem quando ocorre falha e quando `--record-screen` está habilitado.

### Providers (cloud)

- Em `lt`, `bs` e `sauce`, as evidências (vídeo/screenshot) geralmente ficam no painel do provider.
- Use o **Build Name** para localizar a execução mais rápido no provider e no histórico do `run_gui`.

## Como reproduzir uma falha (passo a passo)

Quando um teste falhar, siga esta ordem:

1. Rode o teste isolado (um arquivo só).
2. Rode em `--grid local` para diferenciar problema do provider vs problema do teste.
3. Rode sem paralelismo (sem `-n`) para evitar efeitos colaterais.
4. Se for falha intermitente, rode 2 ou 3 vezes seguidas para confirmar se é flakiness.

