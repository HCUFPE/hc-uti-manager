## 1. Database Migration

- [x] 1.1 Adicionar coluna bloqueado_clinico no modelo LeitoEstado (src/models/leito_estado.py)
- [x] 1.2 Gerar arquivo de migração do Alembic contendo a adição da coluna no SQLite

## 2. Backend Implementation

- [x] 2.1 Adicionar rotas POST /bloquear-clinico e /cancelar-reserva-clinica em routers/leito.py
- [x] 2.2 Retornar a flag bloqueado_clinico no método listar_leitos da controller de leitos
- [x] 2.3 Implementar a auto-limpeza de bloqueio genérico no processo de censo de leitos ao detectar ocupação física e registrar histórico correspondente
- [x] 2.4 Ajustar listar_leitos_disponiveis na controller de solicitações para ocultar leitos com bloqueio ativo para o Bloco Cirúrgico
- [x] 2.5 Implementar a lógica de swap/troca de bloqueio no remanejamento de solicitações, registrando o log correspondente no histórico
- [x] 2.6 Ajustar os filtros do BI em src/providers/implementations/indicadores_provider.py para desconsiderar eventos sem prontuário
- [x] 2.7 Incrementar a versão da API para 1.5.0 em src/main.py

## 3. Frontend Implementation

- [x] 3.1 Estilizar destaque visual e legenda 'Reservado p/ Clínico/COB/HEM' no card de leito (frontend/src/components/BedCard.vue)
- [x] 3.2 Incluir botões 'Reservar p/ Clínico/COB/HEM' e 'Cancelar Reserva' no BedCard
- [x] 3.3 Conectar as ações de clique no BedCard com chamadas de API correspondentes no Home.vue e gerenciar o estado local
- [x] 3.4 Incrementar a versão do sistema para 1.5.0 e data de atualização em frontend/src/config/version.ts

## 4. Testing & Verification

- [x] 4.1 Desenvolver casos de testes unitários/integração no backend cobrindo bloqueio, filtragem de elegibilidade e swap
- [x] 4.2 Rodar os testes automatizados locais para certificar estabilidade da versão 1.5.0
