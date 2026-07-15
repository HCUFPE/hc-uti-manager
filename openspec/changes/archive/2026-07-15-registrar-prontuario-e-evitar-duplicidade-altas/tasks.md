## 1. Backend

- [x] 1.1 Modificar `solicitar_alta` em `src/routers/altas.py` para obter o prontuário do leito e passá-lo para `historico.registrar(..., prontuario=prontuario)`.
- [x] 1.2 Modificar `cancelar_alta` em `src/routers/leito.py` para obter o prontuário do leito antes do cancelamento e passá-lo para `historico.registrar(..., prontuario=prontuario)`.
- [x] 1.3 Verificar e garantir que na conclusão automática de alta em `LeitosController`, o prontuário do paciente é gravado corretamente no histórico.
- [x] 1.4 Confirmar e garantir que as ações do NIR (definir destino e marcar como disponível/indisponível) estão gravando o prontuário corretamente no histórico.

## 2. Frontend

- [x] 2.1 Atualizar o modal de solicitar alta em `frontend/src/views/Home.vue` para garantir o uso de um estado reativo de submissão (ex: `submetendoAlta`) e aplicar `:disabled="submetendoAlta"` no botão de confirmação.
- [x] 2.2 Validar e testar a compilação do frontend com `npm run build`.
