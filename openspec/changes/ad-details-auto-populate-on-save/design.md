## Context

Atualmente, o modal de atribuição de perfil solicita a digitação do Login de Rede e depois tenta preencher as caixas de texto de Nome Completo, Lotação e E-mail disparando uma consulta local ao AD (no evento `@blur`). Queremos remover a necessidade dessas caixas de texto e da busca do lado do cliente, passando essa lógica integralmente para a rota `POST /api/admin/perfis`.

## Goals / Non-Goals

**Goals:**
- Buscar dados cadastrais (nome, lotação, e-mail) do Active Directory diretamente no backend no momento do salvamento do perfil.
- Simplificar o formulário do frontend, mantendo apenas Login da Rede e Perfil de Acesso.
- Mudar o texto do botão de ação principal do modal de "Salvar Perfil" para "Salvar Usuário".

**Non-Goals:**
- Alterar as permissões ou perfis de acessibilidade pré-existentes.

## Decisions

### 1. Atualização do Backend (`src/routers/admin.py`)
No endpoint `POST /api/admin/perfis`, se os campos `nome_completo`, `lotacao` ou `email` não forem informados ou vierem vazios na requisição, tentaremos resolvê-los consultando o Active Directory de forma assíncrona usando o `run_in_threadpool`:
```python
if not nome_completo or not lotacao or not email:
    try:
        user_info = await run_in_threadpool(auth_handler.authenticate_user, username, None)
        # Parse e preenchimento dos campos DisplayName, Department e Mail
        ...
    except Exception:
        # Fallback tolerante para evitar falha se o AD estiver inacessível
        pass
```

### 2. Simplificação do Frontend (`frontend/src/views/AdminConfig.vue`)
- Ocultar/remover os elementos `<input>` para Nome Completo, Lotação e E-mail do modal.
- Remover o evento `@blur="buscarUsuarioAD"` do campo de input de Login da Rede.
- Renomear o botão:
```html
<button ...>
  {{ submitting ? 'Salvando...' : 'Salvar Usuário' }}
</button>
```

## Risks / Trade-offs

- **Tolerância a Falhas**: Se o servidor do Active Directory estiver temporariamente indisponível, o salvamento não deve ser abortado. O backend usará blocos `try-except` tolerantes, deixando os dados em branco (ou usando fallbacks mockados) em caso de falha.
