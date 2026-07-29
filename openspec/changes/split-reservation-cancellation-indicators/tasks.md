## 1. Backend Logic Changes

- [x] 1.1 Atualizar `src/controllers/solicitacao_leito_controller.py` para gravar `tipo="cancelamento_solicitante"` nas trocas de paciente em solicitações reservadas e refrasear os textos do histórico de auditoria.
- [x] 1.2 Atualizar `src/controllers/alerta_controller.py` para gerar alertas "Reserva Cancelada pelo Solicitante" para eventos de `tipo="cancelamento_solicitante"`.
- [x] 1.3 Atualizar `src/providers/implementations/indicadores_provider.py` para calcular e expor separadamente `cancelamento_reservas_uti` e `cancelamento_reservas_solicitante`.

## 2. Frontend UI Changes

- [x] 2.1 Atualizar `frontend/src/views/Indicadores.vue` para exibir as duas linhas distintas no resumo de ações operacionais.

## 3. Versioning

- [x] 3.1 Incrementar versão da aplicação para "1.4.11" (ou próximo patch).
