# AGENTS.md

## Perfil e objetivo
- Engenheiro(a) de QA desde 2019, com foco em testes E2E web e mobile usando Selenium + Python/pytest para um e-commerce.
- Prioridade: tornar a suíte mais estável, rápida e fácil de diagnosticar, aproveitando automações e IA (Codex) para reduzir trabalho manual.

## Regras de trabalho
- Use sempre os utilitários de sincronização (`helpers/waiters.py`, `helpers/actions.py`) antes de criar novos `time.sleep`.
- Prefira interações encapsuladas (`safe_click_loc`, `scroll_into_view`, `mobile_click_strict`) e só use `driver.find_element` direto se for trivial.
- Ao criar novos seletores, mantenha-os em `locators/` e reuse padrões existentes; evite XPath frágil e seletores por texto dinâmico.
- Nomeie testes com `test_` e aplique marcadores do `pytest.ini` (ex.: `@pytest.mark.smoke`, `@pytest.mark.mobile`) para facilitar a seleção.
- Evite duplicar passos de navegação: extraia fluxos comuns para helpers e centralize variações por região (Default/Sul).
- Antes de qualquer implementação, me forneça a solução para revisão. Após o meu "ok" você poderá seguir com a alteração.

## Checks rápidos antes de abrir PR
- Smoke web: `pytest -q -m smoke Testes`
- Mobile fatiado: `pytest -q -m "mobile and smoke" Testes_Mobile`
- Caso altere `helpers/actions.py` ou `helpers/waiters.py`, rode pelo menos: `pytest -q Testes\\PROD\\Default\\test_1_userDeslogado.py`
- Registre no resumo de PR quais marcadores rodaram e principais falhas intermitentes observadas.

## Subagents que o Codex deve usar
- **Planner**: gerar plano de testes ou cobertura para uma funcionalidade; paralelize por plataforma (web/mobile) e região (Default/Sul).
- **Selector Doctor**: revisar e propor seletores mais estáveis quando houver flakiness ou muitos `StaleElementReferenceException`.
- **Data Genie**: criar dados de entrada (usuário, endereço, cupom) sintéticos e descartáveis, respeitando formatos atuais do site.
- **Triage Reporter**: resumir falhas recentes, sugerir agrupamentos por sintoma e próximos passos de investigação.
Peça explicitamente pelo subagent adequado sempre que a tarefa envolver essas áreas para ganhar tempo e paralelizar análise. citeturn10view0

## Uso de skills
- Considere os skills do diretório `.agents/skills` antes de criar instruções ad hoc; o Codex só carregará o `SKILL.md` quando o skill for escolhido. citeturn9view0
- Habilite o `$qa-selenium-hardening` ao mexer em interações web/mobile.
- Habilite o `$pytest-runbook` ao criar/ajustar cenários ou ao definir que marcadores rodar.

## Notas sobre AGENTS.md
- O Codex carrega instruções globais e depois as do projeto, caminhando do raiz até o diretório atual; arquivos mais próximos sobrepõem os anteriores. citeturn4view0
- Se surgir a necessidade de escopo diferente para um módulo, crie um `AGENTS.override.md` na pasta-alvo.

## Modelo e segurança
- Prefira modelos de raciocínio (gpt-5.4) para alterações amplas ou diagnósticos; use variantes menores apenas para geração repetitiva.
- Evite incluir credenciais reais nos testes; use dados falsos e limpe quaisquer dumps ou screenshots que contenham informações sensíveis.