# Perguntas frequentes

Este FAQ foca no uso do `run_gui` (executor visual).

## Qual comando usar para rodar um smoke rápido?

```bash
pytest -q -m smoke Testes
```

## Qual comando usar para rodar a regressão?

```bash
pytest -q -m regressao Testes
```

## Como rodar smoke mobile?

```bash
pytest -q -m "mobile and smoke" Testes_Mobile
```

## Como rodar regressão mobile?

```bash
pytest -q -m "mobile and regressao" Testes_Mobile
```

## Como apontar para outro site sem mexer no .env?

Você tem duas opções:

- Via terminal (CLI): `--base-url`.
- Via `run_gui`: preencher a **URL custom**.

Exemplo (CLI):

```bash
pytest -q Testes/PROD/Default/test_1_userDeslogado.py --grid local --base-url https://seu-site
```

## Onde ficam os marcadores (markers)?

No arquivo `pytest.ini`. Use markers para facilitar seleção (`-m`) e organização.

## O GUI não abre

Verifique:

- A pasta `.venv` existe e as dependências foram instaladas (`pip install -r requirements.txt`).
- Você está executando `run_gui.bat` (Windows) ou `run_gui.sh` (Linux/macOS).

## Como escolher os testes mais rápido (sem procurar arquivo por arquivo)?

Use o campo **Plano de teste**.

- Ele seleciona um conjunto pronto de testes (ex.: Smoke, Regressão).
- Esses conjuntos vêm do arquivo `test_plans.json`.

## Como usar o filtro de testes?

Use **Filtrar testes** para buscar pelo nome exibido (ex.: `checkout`, `carrinho`, `mobile`).

- O filtro só muda o que aparece na lista. Ele não altera o projeto nem “cria” testes.

## O que significa “Limpar seleção ao executar”?

Quando marcado, após iniciar a execução o `run_gui` desmarca os testes selecionados.

Use isso quando você costuma rodar vários lotes diferentes em sequência e não quer reutilizar a seleção anterior sem querer.

## Visualização (Desktop/Mobile): o que muda?

- **Desktop**: o painel esquerdo mostra apenas testes de `Testes/`. O campo **Resolução Desktop** fica habilitado e **Dispositivos Mobile** fica desabilitado.
- **Mobile**: o painel esquerdo mostra apenas testes de `Testes_Mobile/`. O campo **Dispositivos Mobile** fica habilitado e **Resolução Desktop** fica desabilitado.

Importante: ao trocar a visualização, a lista é recarregada e a seleção anterior não é mantida.

## Plataforma: o que é “local”, “lt”, “bs” e “sauce”?

- `local`: executa no seu computador.
- `lt`: LambdaTest (execução remota).
- `bs`: BrowserStack (execução remota).
- `sauce`: Sauce Labs (execução remota).

## Como configurar “Ambiente” e “URL custom”?

- `prod`: usa `URL`.
- `stg1`: usa `URL_STG1` do `.env`.
- `stg2`: usa `URL_STG2` do `.env`.
- `outro`: exige uma URL preenchida em **URL custom**.

Se **URL custom** estiver preenchida, ela sobrescreve o ambiente selecionado.

## Timeout: qual o impacto?

O **Timeout** define por quanto tempo o teste vai esperar por algo antes de falhar (ex.: um botão ficar clicável).

- Timeout maior: mais tolerante a lentidão, mas pode demorar mais para “falhar de vez”.
- Timeout menor: falha mais rápido, mas pode aumentar flakiness em ambiente instável.

## O que é “Headless” no run_gui?

Headless roda sem abrir a janela do navegador.

- É mais usado em `local`.
- Regra do `run_gui`: se Headless estiver marcado e a **Plataforma** não estiver definida, o GUI força `local`.

## Para que serve “Pré-visualizar comando”?

Serve para conferir exatamente o que o `run_gui` vai executar (testes selecionados, opções e marcadores do plano).

Também é útil para diagnosticar “por que rodou diferente do esperado” antes de clicar em **Executar**.

## Histórico: como usar para entender uma falha?

No **Histórico** você consegue filtrar execuções por:

- Status (passed/failed).
- Build Name.
- Período (Data Início / Data Fim) e filtro rápido **Hoje**.

Quando um teste falha, pode aparecer o botão **ver log**:

- Ele mostra um trecho do erro (recorte) para facilitar identificar a causa.
- Nem toda falha terá “ver log” disponível (depende do que foi capturado no resultado).

## Onde ficam as evidências locais e o histórico?

- Evidências locais (falhas): `evidencias_local/` (ou a pasta definida por `PYTEST_ARTIFACTS_ROOT`).
- Histórico do `run_gui`: arquivo `.test_history.json` na raiz do projeto.
