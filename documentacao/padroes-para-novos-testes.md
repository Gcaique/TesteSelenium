# Padrões para novos testes

Este documento define o padrão para escrever testes novos neste repositório, com foco em:

- estabilidade (menos flakiness),
- velocidade (evitar esperas desnecessárias),
- diagnóstico (falhas fáceis de entender e reproduzir),
- manutenção (mudanças no site exigem poucas alterações).

Objetivo: manter testes estáveis, rápidos e fáceis de diagnosticar.

## Convenções

- Nome de arquivo: `test_*.py`
- Nome de teste: `test_<descricao_curta>`
- Use markers do `pytest.ini` (ex.: `@pytest.mark.smoke`, `@pytest.mark.regressao`, `@pytest.mark.mobile`, `@pytest.mark.checkout`).

Regras recomendadas:

- Um teste deve validar 1 fluxo principal (arrange/act/assert). Se ficar longo, extraia para helpers.
- Evite asserts genéricos. Prefira mensagens claras e verificações que indiquem o "porquê" da falha.
- Use `base_url` (fixture) para navegação base; evite hardcode de URLs no teste.

## Marcação recomendada (smoke e regressão)

Recomendação:

- Todo teste que faz parte da suíte principal deve ter `@pytest.mark.regressao`.
- Um subconjunto pequeno e crítico também recebe `@pytest.mark.smoke`.

Isso facilita:

- rodar `smoke` rápido para sanity/diagnóstico;
- rodar `regressao` para cobertura completa.

Boas práticas de marcação:

- `smoke` deve ser pequeno e representativo (fluxos críticos).
- `regressao` pode ser amplo (cobertura funcional).
- Combine com `default`/`sul` e com áreas (`cart`, `checkout`, etc.) quando fizer sentido.

## Reuso de helpers e waits

Antes de criar `time.sleep`, procure e reuse:

- `helpers/waiters.py`: funções de sincronização (`visible`, `clickable`, etc.).
- `helpers/actions.py`: cliques e preenchimentos robustos (`safe_click_loc`, `scroll_into_view`, etc.).

Recomendação:

- Prefira helpers encapsulados para reduzir flakiness e repetição.
- Use `WebDriverWait` e condições (expected conditions), não sleeps fixos.
- Se um clique é intermitente (intercept/stale), prefira as funções seguras em `helpers/actions.py` em vez de replicar retry no teste.
- Se você precisar de um novo comportamento (ex.: "clicar e aguardar sumir"), adicione no helper e reaproveite.

## Locators (seletores)

Ao criar novos seletores:

- Mantenha-os em `locators/`.
- Reuse padrões existentes.
- Evite XPath frágil e seletor por texto dinâmico.

Regras recomendadas:

- Prefira seletores estáveis (id, data-attributes, atributos não dinâmicos).
- Se o seletor muda muito por região (Default/Sul), centralize a lógica no helper de região, não em vários testes.
- Se precisar de XPath, mantenha-o curto e baseado em estrutura estável (evite indexes e textos variáveis).

## Estrutura recomendada de teste

Pense em cada teste como um passo a passo do que um usuário faria no site.

Estrutura simples (3 partes):

- Preparar: abrir o site e deixar tudo pronto (ex.: escolher região, fazer login se precisar).
- Executar: fazer as ações (clicar, preencher campos, buscar produto, adicionar ao carrinho).
- Verificar: conferir se o resultado aconteceu (ex.: apareceu uma mensagem, o carrinho tem itens, a página certa abriu).

Sempre que possível:

- Prefira verificações fáceis de entender (ex.: "estou logado", "o carrinho não está vazio") usando helpers, para evitar repetição.
- Em falhas, pense no que vai facilitar investigar: evidência (GIF local quando habilitado) e uma mensagem de erro clara.

## Exemplo mínimo (template)

```python
import pytest

from helpers.actions import safe_click_loc
from locators.common import BTN_EXEMPLO


@pytest.mark.regressao
@pytest.mark.smoke
@pytest.mark.default
def test_exemplo_fluxo(driver, base_url, wait):
    # O fixture `wait` respeita o `--timeout` configurado (ex.: via run_gui).
    # Assim, você evita hardcode de timeout dentro do teste.
    driver.get(base_url)
    safe_click_loc(driver, wait, BTN_EXEMPLO)

    # Assert (verificação): valide o resultado esperado.
    # Exemplo simples: conferir se você chegou na URL correta após a ação.
    assert "exemplo" in driver.current_url, "Era esperado navegar para a página de exemplo."
```

## Quando usar desktop vs mobile

- Desktop: validar fluxos principais e regressão funcional.
- Mobile: validar comportamento responsivo e fluxos críticos em device, com atenção à sincronização.

Regras práticas:

- Mobile tende a ser mais sensível a sincronização. Prefira waits explícitos e interações robustas.
- Se o mesmo fluxo existe em Desktop e Mobile, mantenha a maior parte da lógica em helpers e use variações mínimas no teste.
