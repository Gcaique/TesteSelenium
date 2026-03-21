---
name: pytest-runbook
description: Ative ao escrever ou ajustar cenários de teste; ajuda a escolher marcadores, dados e comandos pytest corretos para este repositório.
---

## Contexto rápido
- `pytest.ini` define marcadores principais: smoke, default, sul, deslogado, logado, mobile, dashboard, favoritos, cart, checkout, redefinir_senha, lp, refazer, mapa.
- Testes web vivem em `Testes/`; mobile em `Testes_Mobile/`.

## Fluxo recomendado
1) Identifique plataforma e região e aplique o marcador correspondente (ex.: `@pytest.mark.mobile` + `@pytest.mark.sul`).
2) Reutilize fixtures/steps existentes antes de duplicar lógica.
3) Comandos rápidos:
   - Smoke web: `pytest -q -m smoke Testes`
   - Smoke mobile: `pytest -q -m "mobile and smoke" Testes_Mobile`
   - Foco em um caso: `pytest -q path/to/test_file.py -k <trecho_nome>`
4) Ao adicionar novo helper ou selector, inclua pelo menos um teste marcado como smoke (quando aplicável) para pegar regressões básicas.
5) Em falha recorrente, capture traceback e associe ao marcador; proponha nova marca `xfail` só com justificativa clara.

## Saídas esperadas
- Lista curta de comandos sugeridos para o trabalho atual.
- Mapa de marcadores aplicados e motivo.
- Notas sobre dados de teste e resets necessários entre cenários.
