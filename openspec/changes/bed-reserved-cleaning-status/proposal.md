## Why

Quando um leito é reservado no sistema (ex: para paciente cirúrgico ou transferência da UTI), mas o status no AGHU indica que o leito ainda está em processo de "Limpeza / Higienização", o leito hoje sobrescreve totalmente a badge para "Reservado". Isso omite uma informação operacional valiosa para a equipe de enfermagem/plantão: saber que o leito está reservado **e ao mesmo tempo** entender que ele ainda passa por higienização física.

## What Changes

- **Preservação e Exibição Visual de Higienização no Leito Reservado**:
  - Manter a badge principal como `Reservado` (roxa).
  - Adicionar abaixo do badge principal, em fonte menor (`text-xs` / `text-[11px]`) e fora do badge, um indicador visual textual em tom discreto de alerta/higienização: `🧹 Leito em Higienização (AGHU)`.
- **Simulação em Homologação**:
  - Implementar uma chave/parâmetro de simulação temporária em Homologação para que um dos leitos fique forçadamente com reserva + status AGHU de limpeza, permitindo visualização imediata da interface.
- **Deploy Inicial Restrito a Homologação**:
  - Garantir a entrega inicial exclusivamente no ambiente de Homologação (`10.34.0.151`) para validação visual pelo usuário antes da produção.

## Capabilities

### New Capabilities
- Nenhum novo módulo top-level.

### Modified Capabilities
- Nenhuma modificação que altere regras de negócio de alto nível.

## Impact

- `frontend/src/components/BedCard.vue`: Renderização da sub-legenda de higienização sob o badge de status.
- `src/controllers/leitos_controller.py`: Repasse da flag original de status do AGHU (`status_aghu_original` ou `status == 'higienizacao'`) junto ao leito reservado.
- `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`: Registro da nova regra visual.
