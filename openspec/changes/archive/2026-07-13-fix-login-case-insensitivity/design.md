## Context

O login bem-sucedido no Active Directory retorna um dicionário de informações do usuário, contendo a chave `"username"`. O valor associado é exatamente a string digitada pelo usuário no formulário de login do frontend (que pode conter caracteres maiúsculos). No banco SQLite, a tabela `usuarios_perfis` armazena todos os registros em letras minúsculas. Como as consultas em SQLite são case-sensitive por padrão, a busca pelo perfil do usuário falha quando a capitalização não coincide.

## Goals / Non-Goals

**Goals:**
- Garantir que o nome de usuário autenticado seja tratado uniformemente em minúsculas antes de qualquer busca de perfil no banco de dados local.
- Prevenir que o usuário caia no perfil fallback "Comum" se tiver digitado letras maiúsculas no formulário de login.

**Non-Goals:**
- Mudar o comportamento de autenticação do LDAP/AD.
- Alterar as tabelas ou esquemas do banco.

## Decisions

- **Modificação em `src/routers/auth.py`:**
  - Logo após obter o objeto `user` retornado por `authenticate_user`, realizar a conversão de `user["username"]` para minúsculas:
    ```python
    user["username"] = user["username"].strip().lower()
    ```
  - Isso garante que a linha seguinte:
    ```python
    stmt = select(UsuarioPerfil).where(UsuarioPerfil.username == user["username"])
    ```
    realize a busca no banco SQLite com o valor estritamente normalizado.

## Risks / Trade-offs

- **Risco:** Incompatibilidade caso algum usuário estivesse cadastrado em maiúsculas na tabela local.
- **Mitigação:** Confirmamos via script de diagnóstico que todos os 68 usernames da tabela `usuarios_perfis` na VM de produção já estão gravados estritamente em minúsculas. Portanto, o risco é zero.
