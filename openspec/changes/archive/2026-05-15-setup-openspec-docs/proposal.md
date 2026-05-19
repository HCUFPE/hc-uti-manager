## Why

A aplicação atual precisa ter seus domínios e regras de negócio mapeados utilizando o framework OpenSpec para viabilizar o desenvolvimento orientado a especificações (spec-driven development). Isso garante uma melhor governança, planejamento de mudanças futuras e alinhamento com a arquitetura definida (Backend monolítico FastAPI + Frontend Vue 3 Vite).

## What Changes

- Inicialização da base de especificações (specs) do OpenSpec para os módulos fundamentais do sistema.
- Definição arquitetural inicial nos documentos de design.
- Documentação formal dos domínios já estabelecidos ou em desenvolvimento, convertendo o conhecimento atual para o formato de Capabilities.

## Capabilities

### New Capabilities
- `faturamento-sus`: Geração de AIH, BPA e arquivos magnéticos.
- `inventario-estoque`: Controle de dados de estoque do AGHU/Oracle.
- `internacao-leitos`: Gestão de censo, relatórios de UTI e clínica médica.
- `solicitacao-leitos`: Gerenciamento de requisições de leitos de UTI pelo Bloco Cirúrgico (BC), Centro Obstétrico (COB) e Hemodinâmica (HEM).
- `medicamentos`: Controle de dispensação e antimicrobianos.
- `bi-dashboard`: Integração com Metabase para análise de dados.
- `prontuario`: Dados clínicos e históricos de atendimentos.

### Modified Capabilities
- N/A

## Impact

- **Documentação**: Criação de arquivos `.md` detalhando as especificações de cada capability na pasta `openspec/specs/`.
- **Governança**: Padroniza a forma como novas features serão implementadas no futuro (através do fluxo `/opsx-propose` e `/opsx-apply`).
- **Código**: Nenhuma alteração direta no código do produto (frontend/backend) neste primeiro momento, as mudanças limitam-se ao repositório de documentação OpenSpec.
