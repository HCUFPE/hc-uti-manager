## Context

Fazer alarme sonoro recorrente de 30s em 30s no Modo TV/Dashboard Geral para alertas não lidos específicos da UTI.

## Goals / Non-Goals

**Goals:**
- Implementar `unreadAlertsCount` como uma variável reativa em `Home.vue`.
- Criar a função assíncrona `fetchUnreadAlertsCount` para bater no endpoint `/api/alertas/unread-count`.
- Modificar `verificarETocarSom` em `Home.vue` para ser assíncrona, chamar `fetchUnreadAlertsCount` e tocar o alerta sonoro se `unreadAlertsCount.value > 0 && authStore.isUTI`.

## Decisions

- **Modificação em `frontend/src/views/Home.vue`:**
  - Adicionar o estado reativo `const unreadAlertsCount = ref(0);`.
  - Criar `fetchUnreadAlertsCount()`.
  - Atualizar `verificarETocarSom()` para:
    ```typescript
    const verificarETocarSom = async () => {
      await fetchUnreadAlertsCount();
      const temCirurgiaPendente = leitos.value.some(
        (l) => l.proximoPaciente && l.cirurgiaFinalizada && !l.encaminhamentoLiberado
      );
      const temAlertaUtiPendente = unreadAlertsCount.value > 0;
      if ((temCirurgiaPendente || temAlertaUtiPendente) && authStore.isUTI) {
        tocarAlertaSonoro();
      }
    };
    ```
