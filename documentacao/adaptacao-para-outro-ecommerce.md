# Adaptação para outro e-commerce

Este guia explica como usar este projeto como base para automatizar outro e-commerce.

## Ideia principal

Você não precisa reescrever tudo. A parte "pronta" do projeto (execução via terminal/GUI, estrutura, drivers e padrões) já funciona. O que muda de um e-commerce para outro é, principalmente:

- os botões/campos/links (seletores em `locators/`);
- o caminho do usuário (fluxos em `helpers/`);
- os dados usados nos testes (usuário, endereço, cupom).

## Checklist de adaptação (passo a passo)

### 1) Apontar para o novo site (URL)

Você precisa definir a URL base do novo e-commerce.

Formas de fazer isso:

- Opção A (recomendado): configurar no `.env`.
  - `prod`: usa `URL`
  - `stg1`: usa `URL_STG1`.
  - `stg2`: usa `URL_STG2`.
- Opção B: passar no terminal (CLI) sem mexer no `.env`:
  - `--base-url https://seu-site`
- Opção C: usar a **URL custom** no `run_gui` (boa para começar rápido).

### 2) Atualizar os seletores (locators)

Locators são os "endereços" dos elementos na tela (botões, campos, links).

O que fazer:

- Crie ou ajuste os arquivos em `locators/` para as telas do novo site.
- Prefira seletores estáveis: `id`, `data-*`, atributos fixos.
- Evite seletores frágeis: XPath longo, texto que muda, índices.

### 3) Atualizar os fluxos reutilizáveis (helpers)

Helpers são passos comuns que se repetem em vários testes, por exemplo:

- login;
- escolher região (Default/Sul);
- buscar produto;
- adicionar ao carrinho;
- iniciar checkout.

O que fazer:

- Ajuste os helpers para refletir o fluxo real do novo site.
- Evite colocar "passo a passo" do site direto no teste. Centralize em `helpers/` para facilitar manutenção.

### 4) Atualizar dados de teste (usuário, endereço, cupom)

O que fazer:

- Use dados sintéticos (fake) e descartáveis.
- Evite credenciais reais e dados pessoais.
- Se o site exigir login, configure `USERNAME` e `PASSWORD` no `.env` (ou passe via CLI).

### 5) Usar marcadores (markers) para organizar

Markers ajudam a rodar só um tipo de teste. Recomendação:

- Marque testes principais como `@pytest.mark.regressao`.
- Marque poucos testes críticos como `@pytest.mark.smoke`.
- Reuse markers existentes (`mobile`, `default`, `sul`, `checkout`, etc.).
- Se criar marker novo, registre no `pytest.ini`.

### 6) Ajustar planos do GUI (Smoke / Regressão)

O `run_gui` usa `test_plans.json` para montar planos prontos.

O que fazer:

- Atualize `test_plans.json` com os paths dos testes do novo site.
- Garanta que o plano Smoke tenha poucos testes (rápido).
- Garanta que o plano Regressão tenha a cobertura completa.

## Primeiro objetivo (MVP)

Antes de criar dezenas de testes, valide primeiro o "mínimo que prova que a base funciona":

- Abrir a home do novo site.
- Fechar/aceitar cookies e popups (se existir).
- Login (se existir).
- Adicionar item ao carrinho.
- Iniciar checkout (mesmo que não finalize).

## Dica (como pensar na estrutura)

Pense no projeto como camadas:

- `locators/`: o que clicar/encontrar na tela.
- `helpers/actions.py` e `helpers/waiters.py`: como clicar/esperar de forma estável.
- `helpers/`: passos comuns do site (login, carrinho, checkout).
- `Testes/` e `Testes_Mobile/`: os testes em si (verificações e variações).

