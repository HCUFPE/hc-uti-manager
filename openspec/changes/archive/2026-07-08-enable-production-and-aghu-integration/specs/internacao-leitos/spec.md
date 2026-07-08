## ADDED Requirements

### Requirement: Purga de Dados de Homologação/Simulação
O sistema MUST expurgar de forma permanente todos os dados fictícios/simulados da base local SQLite na ativação da versão de produção, incluindo o expurgo dos usuários de teste pré-definidos (`admin`, `bloco`, `nir`, `uti`) do banco de dados.

#### Scenario: Purga na inicialização em produção
- **WHEN** o sistema é inicializado em modo de produção
- **THEN** os usuários mockados e históricos de simulação SHALL ser excluídos de forma irreversível da base SQLite, permitindo apenas logins via Active Directory (LDAP).

## MODIFIED Requirements

### Requirement: Gestão de Leitos
O sistema MUST gerenciar o censo de internação obtendo as informações reais em tempo real a partir do banco de dados do AGHU (PostgreSQL), desabilitando qualquer geração de dados fictícios ou simulação em memória. O sistema MUST considerar como leitos disponíveis para reserva aqueles com status "Livre", "Alta", "Limpeza" ou "Higienização".

#### Scenario: Ocupação de Leito
- **WHEN** um paciente é admitido na unidade e associado ao leito
- **THEN** o sistema atualiza o status do leito para ocupado e exibe no mapa de leitos

#### Scenario: Reserva de Leito em Higienização
- **WHEN** um usuário busca leitos disponíveis para reserva de uma solicitação
- **THEN** os leitos com status "Limpeza" e "Higienização" também são listados como opções válidas
