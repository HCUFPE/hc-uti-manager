## 1. Backend Implementation

- [x] 1.1 Atualizar a rota `DELETE /api/altas/{alta_id}` em `src/routers/altas.py` para permitir os perfis `Role.NIR` e `Role.NIR_ADMIN`, aceitar o query param `motivo`, e registrar no histórico de ações a string indicando que foi `"cancelada pelo NIR"`.
- [x] 1.2 Ajustar `src/controllers/alerta_controller.py` para identificar o cancelamento feito pelo NIR (verificando a presença de `"pelo NIR"` nos detalhes) e gerar o alerta correspondente `"Cancelamento de Alta pelo NIR"` direcionado à UTI (`perfil_alvo = None`).

## 2. Frontend Implementation

- [x] 2.1 Adicionar o botão "Cancelar Solicitação" na visualização do NIR em `Altas.vue` ao lado do botão "Indicar Destino".
- [x] 2.2 Implementar o modal de confirmação de cancelamento em `Altas.vue` contendo o select de motivo com a opção `"Leito de Enfermaria Indisponível"`.
- [x] 2.3 Implementar a chamada de API de cancelamento `DELETE /api/altas/{alta_id}?motivo={motivo}` ao confirmar o modal no frontend.

## 3. Verification

- [x] 3.1 Verificar o funcionamento completo do cancelamento da alta pelo NIR via frontend.
- [x] 3.2 Validar se o alerta `"Cancelamento de Alta pelo NIR"` foi gerado corretamente para a UTI e o registro de histórico foi criado.
