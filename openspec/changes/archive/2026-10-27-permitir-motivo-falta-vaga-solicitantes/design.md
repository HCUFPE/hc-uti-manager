# Design: Disponibilização do Motivo "Falta de vaga de UTI" para Solicitantes

## Context

No fluxo atual do frontend (`frontend/src/views/Solicitacoes.vue`), a constante `MOTIVOS_CANCELAMENTO` contém os motivos padrão disponibilizados aos setores solicitantes (BC, COB e HEM). A computed property `motivosAtuais` restringe a exibição da opção `"Falta de vaga de UTI"` apenas quando o usuário possui perfil de `UTI` ou `Administrador`:

```typescript
const MOTIVOS_CANCELAMENTO = [
  'Cirurgia suspensa por outros motivos',
  'Paciente encaminhado para enfermaria de origem após a cirurgia',
  'Alteração do mapa cirúrgico',
  'Paciente já ocupa um leito na UTI'
];

const motivosAtuais = computed(() => {
  if (isCancelamentoReserva.value) {
    return MOTIVOS_CANCELAMENTO_RESERVA;
  }
  if (authStore.isUTI && !authStore.isAdmin) {
    return ['Falta de vaga de UTI', 'Paciente já ocupa um leito na UTI'];
  }
  if (authStore.isAdmin) {
    return [...MOTIVOS_CANCELAMENTO, 'Falta de vaga de UTI'];
  }
  return MOTIVOS_CANCELAMENTO;
});
```

No backend (`src/routers/solicitacoes_leito.py`), a exclusão/cancelamento da solicitação já permite que o setor criador (`solicitacao.perfil_solicitante == user_grupo`) cancele sua própria solicitação passando qualquer `motivo` via query parameter, registrando o texto formatado no log de auditoria. O provedor de métricas (`src/providers/implementations/indicadores_provider.py`) processa esse texto dinamicamente (`- Motivo: <texto>`) e o agrupa no relatório de indicadores.

## Goals / Non-Goals

**Goals:**
- Adicionar `"Falta de vaga de UTI"` à lista geral de motivos de cancelamento de solicitações (`MOTIVOS_CANCELAMENTO`).
- Ajustar a computed property `motivosAtuais` para que solicitantes (`BC`, `COB`, `HEM`), Administradores e UTI tenham acesso uniforme e consistente ao motivo.
- Manter o histórico de auditoria e os relatórios de indicadores agregando fidedignamente esse motivo quando acionado pelos solicitantes.
- Atualizar a documentação do projeto e registrar a melhoria no `CHANGELOG.md` na versão `1.8.0`.

**Non-Goals:**
- Não alterar a lista de motivos de **Cancelamento de Reserva** (`MOTIVOS_CANCELAMENTO_RESERVA`), que permanece com foco nas regras operacionais e clínicas da UTI.
- Não alterar as regras de cancelamento cruzado: solicitantes só podem cancelar solicitações de sua própria autoria/setor. A UTI permanece com autorização especial para cancelar solicitações pendentes de terceiros sob os motivos `"Falta de vaga de UTI"` ou `"Paciente já ocupa um leito na UTI"`.

## Decisions

### Decisão 1: Inclusão direta em `MOTIVOS_CANCELAMENTO` e simplificação de `motivosAtuais`
- **Alternativa A (Escolhida)**: Adicionar `'Falta de vaga de UTI'` diretamente no array `MOTIVOS_CANCELAMENTO`. Em `motivosAtuais`:
  - Se for cancelamento de reserva física (`isCancelamentoReserva`), retorna `MOTIVOS_CANCELAMENTO_RESERVA`.
  - Se for usuário UTI não administrador, retorna `['Falta de vaga de UTI', 'Paciente já ocupa um leito na UTI']`.
  - Caso contrário (Solicitantes BC/COB/HEM e Administrador), retorna `MOTIVOS_CANCELAMENTO`.
  - *Vantagem*: Elimina a necessidade de concatenar arrays inline para o Administrador e garante que todos os solicitantes tenham a opção disponível de forma transparente.
- **Alternativa B**: Criar condicionais extras por perfil (`isBC`, `isCOB`, etc.).
  - *Desvantagem*: Complexidade desnecessária e maior risco de inconsistências com novos perfis de solicitantes futuros.

### Decisão 2: Preservação da lógica do Backend e Histórico
- A rota `DELETE /api/solicitacoes/{sol_id}` já aceita o query param `motivo` e não possui restrição para o solicitante criador. Não são necessárias mudanças estruturais de schema de banco de dados ou migrações.

## Risks / Trade-offs

- **[Risco de Cancelamentos Indevidos por Falta de Vaga]** → Solicitantes poderiam cancelar cirurgias alegando falta de vaga sem comunicação prévia com a equipe de regulação da UTI.
  - *Mitigação*: O log de histórico registra o operador e setor solicitante que executou o cancelamento, garantindo rastreabilidade e governança clínica para os relatórios do censo e BI.
