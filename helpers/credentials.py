import os


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in ("1", "true", "yes", "y", "on")


def _missing_creds_action(message: str) -> None:
    """
    Chamado quando variaveis de ambiente de credenciais obrigatórias não estão definidas.

    Comportamento padrão: pular o modulo inteiro para evitar falhas "barulhentas" em execuções locais.
    Na CI voce pode forcar falha (em vez de skip) definindo E2E_REQUIRE_CREDS=1.
    """
    if _truthy(os.getenv("E2E_REQUIRE_CREDS")):
        raise RuntimeError(message)

    # Uso no import e comum (constantes VALID_USER/VALID_PASS).
    # allow_module_level=True faz o pytest pular corretamente ainda na fase de coleta.
    import pytest  # type: ignore

    pytest.skip(message, allow_module_level=True)


def get_creds(key: str, *, require_pass: bool = True) -> tuple[str, str]:
    """
    Le credenciais de teste a partir de variaveis de ambiente:
      - E2E_<KEY>_USER
      - E2E_<KEY>_PASS

    Exemplo:
      VALID_USER, VALID_PASS = get_creds("SMOKETESTING")
    """
    norm = (key or "").strip().upper()
    user_env = f"E2E_{norm}_USER"
    pass_env = f"E2E_{norm}_PASS"

    username = (os.getenv(user_env) or "").strip()
    password = (os.getenv(pass_env) or "").strip()

    if not username or (require_pass and not password):
        if require_pass:
            msg = (
                "Credenciais não informadas para os testes. "
                f"Defina {user_env} e {pass_env} no .env (local) ou nos secrets da pipeline."
            )
        else:
            msg = (
                "Usuário de teste não informado. "
                f"Defina {user_env} no .env (local) ou nos secrets da pipeline."
            )
        _missing_creds_action(msg)

    return username, password


def get_user(key: str) -> str:
    """
    Le apenas o usuário (email/cpf/cnpj) para fluxos que nao precisam de senha.
    """
    return get_creds(key, require_pass=False)[0]
