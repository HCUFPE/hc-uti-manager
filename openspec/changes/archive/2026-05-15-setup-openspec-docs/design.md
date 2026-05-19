## Context

O HC-UTI-Manager é uma aplicação monolítica FastAPI (backend) com um frontend SPA Vue 3 (Vite). Para melhorar a governança do projeto e orientar o desenvolvimento com base em documentação estruturada, o repositório adotará o **OpenSpec** (um framework de desenvolvimento baseado em especificações). Atualmente a aplicação atende vários domínios como Faturamento SUS, Internação, Medicamentos, etc., que estão descritos apenas em alto nível em arquivos `.md` (ex: `GEMINI.md`) e no próprio código.

## Goals / Non-Goals

**Goals:**
- Configurar corretamente o diretório `openspec` no repositório.
- Criar a base de documentação das *capabilities* principais (`specs`).
- Preparar a estrutura para que as próximas funcionalidades (ex: integrações com Oracle, notificações) sejam desenvolvidas a partir de changes aprovadas (`/opsx-propose` e `/opsx-apply`).

**Non-Goals:**
- Alterar o código-fonte (backend/frontend).
- Alterar dependências ou infraestrutura.
- Mudar regras de negócio do sistema.

## Decisions

- **Estrutura de Specs por Domínio**: Decidimos mapear cada grande domínio da aplicação (como `faturamento-sus`, `inventario-estoque`, `internacao-leitos`, etc.) como uma *capability* separada no OpenSpec. Isso permite dividir bem as responsabilidades das funcionalidades e gerir os requisitos de maneira isolada.
- **Nível de Detalhamento das Specs Iniciais**: Como estamos documentando uma aplicação já existente, as specs iniciais serão mais abrangentes. Elas descreverão as funcionalidades de alto nível (ex: a rota FastAPI exposta, o modelo de banco).

## Risks / Trade-offs

- **Trabalho excessivo de documentação** → A mitigação é não descer num nível de especificação de código excessivo agora; as especificações serão de alto nível. Funcionalidades futuras (via `changes`) trarão mais detalhes progressivamente.
