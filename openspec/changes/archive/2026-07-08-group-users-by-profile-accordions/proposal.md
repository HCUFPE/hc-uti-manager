## Why

A listagem de usuários com perfis atribuídos na tela de configurações está crescendo e precisa de uma organização mais clara. Agruparemos os usuários por perfil de atuação, juntando o perfil comum com sua versão administrativa (ex: juntar NIR e NIR-Admin, UTI e UTI-Admin). Isso facilitará o controle e a auditoria dos operadores por setor. A interface exibirá a quantidade de usuários por grupo e permitirá expandir/colapsar cada grupo, listando os usuários sempre em ordem alfabética.

Adicionalmente, pré-cadastraremos 21 usuários da regulação (NIR) com perfil `"NIR"`, puxando seus dados reais diretamente do Active Directory, como preparação para a entrada em ambiente de produção.

## What Changes

- **Pré-cadastro de Usuários do NIR**: Criar um script em Python (`scratch/backfill_nir_users.py`) que se conecta ao banco de dados SQLite local na VM, consulta os 21 usuários reais do AD através de LDAP e os insere na tabela `usuarios_perfis` com perfil `"NIR"`.
- **Frontend: Agrupamento em Acordeões**:
  - Atualizar `frontend/src/views/AdminConfig.vue` para agrupar os perfis atribuídos nos seguintes grupos:
    - **NIR / NIR-Admin**
    - **UTI / UTI-Admin**
    - **Bloco Cirúrgico (BC) / BC-Admin**
    - **Hemodinâmica (HEM) / HEM-Admin**
    - **Centro Obstétrico (COB) / COB-Admin**
    - **Administrador**
    - **Comum**
  - Implementar um estado reativo de expansão/colapso para cada grupo, exibindo o número de usuários de cada agrupamento no cabeçalho.
  - Ordenar os usuários dentro de cada grupo em ordem alfabética pelo nome completo.

## Capabilities

### Modified Capabilities
- `usuario-config`: Organização e visualização otimizada de usuários por área (acordeões expansíveis por setor), ordenação alfabética e carga inicial de usuários de produção (NIR).

## Impact

- **Carga de Dados**:
  - Execução de script para inserir a equipe real do NIR.
- **Frontend**:
  - `frontend/src/views/AdminConfig.vue`: Modificar a tabela para agrupar por setor com controle de expansão por cabeçalho e ordenação alfabética.
