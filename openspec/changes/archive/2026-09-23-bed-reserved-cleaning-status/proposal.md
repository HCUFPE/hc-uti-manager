## Why

Quando um leito é reservado no sistema (ex: para paciente cirúrgico ou transferência da UTI), mas o status no AGHU indica que o leito ainda está em processo de "Limpeza / Higienização", o leito hoje sobrescreve totalmente a badge para "Reservado". Isso omite uma informação operacional valiosa para a equipe de enfermagem/plantão: saber que o leito está reservado **e ao mesmo tempo** entender que ele ainda passa por higienização física.

## What Changes

- **Preservação e Exibição Visual de Higienização no Leito Reservado**:
  - Manter o badge principal de status (ex: `Reservado`).
  - Adicionar abaixo do badge principal uma pílula amarela de status (`bg-amber-50 text-amber-700 border-amber-200/80 shadow-sm`) com ícone `ArrowPathIcon` e o texto `Higienização`.
  - Exibir a pílula para qualquer leito reservado (seja de cirurgia ou bloqueio clínico da UTI) quando o status AGHU for limpeza/higienização.

## Capabilities

### New Capabilities
- Nenhum novo módulo top-level.

### Modified Capabilities
- Nenhuma modificação que altere regras de negócio de alto nível.

## Impact

- `frontend/src/components/BedCard.vue`: Renderização da sub-legenda de higienização sob o badge de status.
- `src/controllers/leitos_controller.py`: Repasse da flag original de status do AGHU (`status_aghu_original` ou `status == 'higienizacao'`) junto ao leito reservado.
- `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`: Registro da nova regra visual.
