# Documentacao (Markdown)

Esta documentação descreve como configurar e executar a suite E2E (web e mobile) usando Selenium + Pytest, e como adaptar a base para automatizar outro e-commerce.

## Como navegar

Comece por [SUMARIO.md](SUMARIO.md). Ele lista todas as páginas com links diretos.

## Objetivos

- Permitir que qualquer pessoa consiga rodar a suite localmente e em grids remotos.
- Padronizar como escrever testes (helpers, locators, marcadores) para reduzir flakiness. (Falha intermitente: as vezes passa, as vezes falha, sem mudanca no codigo).
- Explicar o executor visual (`run_gui`) em nivel de uso, sem entrar em detalhes de codigo.

## Atalhos

- Primeira vez: leia **Primeiros passos** e depois **Executando via CLI**.
- Se você vai usar o executor: leia **Executando via GUI (run_gui)**.
- Se você vai adaptar para outro site: leia **Adaptação para Outro E-commerce**.
