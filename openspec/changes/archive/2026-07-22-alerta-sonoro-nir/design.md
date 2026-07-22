## Context

Os alertas sonoros auxiliam na resposta imediata a eventos operacionais críticos. Atualmente, apenas a UTI possui o feedback sonoro na interface. O NIR necessita da mesma funcionalidade para responder agilmente aos alertas emitidos.

## Goals / Non-Goals

**Goals:**
* Habilitar os bipes periódicos (tocarAlertaSonoro) na tela inicial se o usuário logado for do NIR e tiver alertas não lidos.

**Non-Goals:**
* Não alterar o som em si, aproveitando o mesmo método sintético de bipes gerado pelo `AudioContextClass`.

## Decisions

### 1. Atualizar a lógica de gatilho sonoro em `Home.vue`
Em `verificarETocarSom()`, a lógica será expandida:
```typescript
const verificarETocarSom = async () => {
  await fetchUnreadAlertsCount();
  const temCirurgiaPendente = leitos.value.some(
    (l) => l.proximoPaciente && l.cirurgiaFinalizada && !l.encaminhamentoLiberado
  );
  const temAlertaPendente = unreadAlertsCount.value > 0;
  
  const utiDeveTocar = authStore.isUTI && (temCirurgiaPendente || temAlertaPendente);
  const nirDeveTocar = authStore.isNIR && temAlertaPendente;

  if (utiDeveTocar || nirDeveTocar) {
    tocarAlertaSonoro();
  }
};
```

## Risks / Trade-offs

* **[Risk]** Loops infinitos de bipes se o estado do componente não re-renderizar o contador de não lidos.
  * **Mitigation**: O método `fetchUnreadAlertsCount` é assíncrono e atualiza a referência `unreadAlertsCount` antes de verificar o toque.
