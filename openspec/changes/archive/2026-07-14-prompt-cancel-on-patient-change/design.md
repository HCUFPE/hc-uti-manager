## Context

Fluxo de troca de paciente na tela de edição.

## Decisions

### 1. Backend: `src/controllers/solicitacao_leito_controller.py`
Ler a propriedade `cancelar_antiga` e atualizar o paciente anterior para `Cancelada` ou `Pendente` conforme o valor recebido:
```python
status_antiga = "Cancelada" if payload.get("cancelar_antiga", True) else "Pendente"
```

### 2. Frontend: `frontend/src/views/Solicitacoes.vue`
- Adicionar modal `showModalConfirmacaoTrocaProntuario`.
- No método `salvarNova()`, se houver mudança de prontuário, exibir o modal e interromper o envio automático.
- No modal, o usuário escolhe a ação que enviará a flag `cancelar_antiga` correta para o endpoint.
