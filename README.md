# HC UTI Manager

Sistema de gerenciamento de leitos, controle de fluxo de pacientes, monitoramento de tempos de liberação e reserva de vagas para a Unidade de Terapia Intensiva (UTI) do Hospital das Clínicas da UFPE.

---

## 🚀 Visão Geral

O **HC UTI Manager** é uma aplicação web full-stack de alto desempenho projetada para otimizar a coordenação de leitos e o tráfego de pacientes em UTIs. Ele automatiza o fluxo de solicitações de leitos, monitora o tempo decorrido de liberação de leitos (com alertas dinâmicos para a equipe do Núcleo Interno de Regulação - NIR e da UTI) e fornece dados analíticos (indicadores de ocupação, cancelamentos e tempos de espera).

---

## 🛠️ Arquitetura e Estrutura de Pastas

A aplicação foi estruturada segundo uma arquitetura monolítica desacoplada, dividindo claramente as responsabilidades de backend, banco de dados e interface.

```
HC-UTI-Manager/
├── alembic/              # Migrações do banco de dados (SQLite local)
├── docs/                 # Documentação detalhada da arquitetura e fluxos
├── frontend/             # Single-Page Application (Vue 3, TypeScript, Vite)
├── openspec/             # Especificações funcionais dos fluxos e mudanças do projeto
├── src/                  # Backend assíncrono (Python 3.10+, FastAPI)
│   ├── auth/             # Módulo de autenticação (JWT, AD LDAP e Mock para dev)
│   ├── controllers/      # Camada de lógica de negócio e regras do fluxo
│   ├── helpers/          # Utilitários de strings, formatação e tempo
│   ├── models/           # Modelos de dados SQLAlchemy
│   ├── providers/        # Acesso a dados e integrações (Postgres/Oracle do AGHU)
│   ├── resources/        # Pools de conexão e inicialização de banco de dados
│   ├── routers/          # Definições de endpoints HTTP e schemas Pydantic
│   └── main.py           # Ponto de entrada do backend e servidor de arquivos estáticos
├── Dockerfile            # Configuração de build multi-stage para Docker/Podman
├── docker-compose.yaml   # Orquestração do container de backend e Nginx reverso
└── hc-uti.service        # Arquivo de serviço do Systemd para a VM de produção
```

---

## ⚙️ Funcionalidades Principais

- **Painel de Leitos (Censo UTI):** Visualização em tempo real do estado de ocupação de cada leito, com informações completas do paciente, necessidade de isolamento e status.
- **Gerenciador de Solicitações:** Painel para o NIR gerenciar pedidos de leito UTI com níveis de prioridade de **P1 a P10**.
- **Controle de Reservas e Conflitos:** Inteligência para evitar conflitos de reserva de leito (ex: não permitir novas reservas automáticas para leitos já ocupados ou reservados).
- **Controle de Tempo de Liberação:** Cronômetro regressivo/progressivo inteligente para acompanhar o tempo de transferência após a alta do leito ser sinalizada.
- **Autenticação LDAP/Active Directory:** Login seguro integrado com o diretório ativo corporativo do hospital, além de fallback automático para desenvolvimento local.
- **Dashboard de Indicadores:** Métricas consolidadas sobre taxa de ocupação, tempo médio de espera, cancelamentos de reserva e fluxo de altas.

---

## 🖥️ Instalação e Execução

### Ambiente de Desenvolvimento Local

1. **Requisitos:** Python 3.10+ e Node.js 20+.
2. **Backend:**
   - Crie um arquivo `.env` baseado no `.env.example`.
   - Crie o ambiente virtual e instale as dependências:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     ```
   - Execute as migrações do banco de dados:
     ```bash
     alembic upgrade head
     ```
   - Inicie o backend em modo de recarregamento rápido:
     ```bash
     uvicorn src.main:app --reload
     ```
3. **Frontend:**
   - Vá para o diretório do frontend e instale as dependências:
     ```bash
     cd frontend
     npm install
     ```
   - Inicie o servidor de desenvolvimento Vite:
     ```bash
     npm run dev
     ```

---

## 📦 Produção e Deployment (VM)

O deployment da aplicação na máquina virtual de produção (`10.34.0.192`) é gerenciado de forma containerizada usando **Podman Compose** e **Systemd**:

1. **Build Multi-stage (`Dockerfile`):** O build compila o frontend Vue, copia os arquivos otimizados gerados para o diretório `/src/static/dist` do FastAPI, e empacota o backend Python em uma imagem de runtime leve.
2. **Serviço do Systemd (`hc-uti.service`):** Configura a inicialização automática do container no boot da máquina virtual e facilita os comandos de reinício e monitoramento de logs (`systemctl restart hc-uti`).