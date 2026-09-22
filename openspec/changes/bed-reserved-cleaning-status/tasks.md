## 1. Backend & Frontend Implementation

- [ ] 1.1 Injetar a flag `statusEmHigienizacao` (ou `status_aghu == 'higienizacao'`) nos payloads de leitos em `src/controllers/leitos_controller.py`.
- [ ] 1.2 Atualizar `frontend/src/components/BedCard.vue` para renderizar o texto em fonte menor `Higienização` (com ícone e estilo discreto) abaixo da badge `Reservado` quando o leito estiver reservado e em higienização.
- [ ] 1.3 Adicionar simulação em Homologação (ex: injetar estado de higienização simulado para leito reservado em ambiente de teste).

## 2. Documentação & Requisitos

- [ ] 2.1 Atualizar `docs/projeto_inicial/02-requisitos.md` e `CHANGELOG.md`.

## 3. Deploy & Validação em Homologação

- [ ] 3.1 Fazer build do frontend (`npm run build`).
- [ ] 3.2 Executar o script `scratch/deploy_homologacao.py` para publicar na VM de Homologação (`10.34.0.151:8080`).
- [ ] 3.3 Apresentar ao usuário para validação visual.
