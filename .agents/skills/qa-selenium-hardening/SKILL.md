---
name: qa-selenium-hardening
description: Use when criando ou ajustando interações Selenium/Pytest para minimizar flakiness em web e mobile.
---

## Quando ativar
- Ajustes em `helpers/actions.py`, `helpers/waiters.py` ou novos helpers de interação.
- Criação de casos de teste com cliques, scroll ou inputs sensíveis a timing.
- Investigação de falhas intermitentes (stale element, intercepted click, tempo de espera insuficiente).

## Checklist
1) Ler rapidamente `helpers/actions.py` e `helpers/waiters.py` para reaproveitar wrappers existentes (ex.: `safe_click_loc`, `scroll_into_view`, `mobile_click_strict`).
2) Preferir `WebDriverWait` encapsulado; evitar `time.sleep` salvo para backoffs curtos explícitos (<0.3s) e sempre justificar.
3) Sempre tente:
   - Localizador em `locators/`; evitar XPath baseado em texto ou posição se houver id/class estável.
   - `visible()`/`clickable()` antes de interações diretas.
4) Para mobile, sempre considerar `mobile_click_strict` antes de criar novos gestos; usar `tap_element` apenas se não houver alternativa.
5) Ao tocar `helpers/actions.py`:
   - Garanta fallback JS click e scroll para centralização.
   - Cubra com um teste de fluxo curto (`pytest -q Testes\\PROD\\Default\\test_1_userDeslogado.py`).
6) Registrar no resumo: seletor utilizado, motivo da escolha, e qualquer timeout customizado.

## Saídas esperadas
- Código com interações idempotentes e sem sleeps longos.
- Comentário curto justificando timeouts fora do padrão.
- Lista das rotas/testes usados para validar a mudança.
