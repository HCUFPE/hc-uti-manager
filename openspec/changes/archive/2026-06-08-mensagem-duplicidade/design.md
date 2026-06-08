## Context

Atualmente o backend retorna um texto informativo detalhado sobre a solicitação duplicada, mas o frontend exibe apenas o texto padrão estático genérico `'Erro ao salvar solicitação.'` em seu bloco `catch`.
O usuário solicitou que a mensagem correta ao tentar cadastrar uma duplicata seja: `"Solicitação para este prontuário já inserida."`.

## Goals / Non-Goals

**Goals:**
- Ajustar a mensagem no backend.
- Exibir dinamicamente o detalhe do erro do backend no frontend.

## Decisions

### 1. Backend
- Alterar a `HTTPException` em `criar_solicitacao`:
  ```python
  raise HTTPException(
      status_code=400, 
      detail="Solicitação para este prontuário já inserida."
  )
  ```

### 2. Frontend
- Alterar `salvarNova` em `frontend/src/views/Solicitacoes.vue`:
  ```javascript
  toast.error(error.response?.data?.detail || 'Erro ao salvar solicitação.');
  ```

## Risks / Trade-offs

- Nossos testes automatizados precisam ser adaptados para a nova mensagem de assertiva.
