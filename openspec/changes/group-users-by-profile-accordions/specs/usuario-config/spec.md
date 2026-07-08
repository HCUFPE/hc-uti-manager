## MODIFIED Requirements

### Requirement: Visualização Agrupada e Colapsável de Usuários
A listagem de usuários nas configurações deve ser organizada em acordeões reativos agrupando perfis semelhantes por área de atuação.

#### Scenario: Visualização em acordeão com contagem e ordenação alfabética
- **WHEN** a tela de gerenciamento de perfis for carregada
- **THEN** os usuários SHALL ser agrupados nos seguintes blocos por setor:
  - NIR / NIR-Admin
  - UTI / UTI-Admin
  - Bloco Cirúrgico (BC) / BC-Admin
  - Hemodinâmica (HEM) / HEM-Admin
  - Centro Obstétrico (COB) / COB-Admin
  - Administrador
  - Comum
- **THEN** o cabeçalho de cada acordeão SHALL exibir a quantidade de usuários nele
- **THEN** cada bloco SHALL permitir expansão e colapso de forma independente
- **THEN** a lista interna de cada bloco SHALL estar ordenada alfabeticamente de forma crescente (A-Z) pelo Nome Completo (ou username, se nome estiver vazio)

### Requirement: Pré-cadastro de Usuários NIR
A base de dados de produção deve ser inicializada com os usuários da equipe do NIR contendo dados reais consultados no Active Directory.

#### Scenario: Script de carga inicial de produção
- **WHEN** o script de carga do NIR for executado
- **THEN** os 21 usuários especificados da regulação SHALL ser inseridos no banco local como perfil `"NIR"`
- **THEN** as propriedades `nome_completo`, `lotacao` e `email` de cada usuário SHALL ser resolvidas e salvas em tempo real a partir de consulta ao AD
