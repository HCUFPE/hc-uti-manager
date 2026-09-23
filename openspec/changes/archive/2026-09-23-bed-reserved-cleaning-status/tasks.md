## 1. Backend & Frontend Implementation

- [x] 1.1 Injetar a flag `status_aghu_original` (ou `status == 'higienizacao'`) nos payloads de leitos em `src/controllers/leitos_controller.py`.
- [x] 1.2 Atualizar `frontend/src/components/BedCard.vue` para renderizar a pílula visual de status amarela de `Higienização` (com ícone `ArrowPathIcon` e classe pílula) abaixo do badge `Reservado` quando o leito reservado estiver em higienização.
- [x] 1.3 Adicionar simulação em Homologação para validação visual.

## 2. Documentação & Requisitos

- [x] 2.1 Atualizar `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`.

## 3. Deploy & Validação em Homologação

- [x] 3.1 Fazer build do frontend (`npm run build`).
- [x] 3.2 Executar o script `scratch/deploy_homologacao.py` para publicar na VM de Homologação (`10.34.0.151:8080`).
- [x] 3.3 Apresentar ao usuário para validação visual.
