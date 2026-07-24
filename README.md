# HC UTI Manager

Sistema de gerenciamento de leitos, controle de fluxo de pacientes do Bloco Cirúrgico para a UTI, monitoramento de tempos de transferência e alocação de vagas para a Unidade de Terapia Intensiva (UTI) do Hospital das Clínicas da UFPE.

---

## 🚀 Visão Geral

O **HC UTI Manager** é uma aplicação web full-stack projetada para otimizar o fluxo de encaminhamento de pacientes do Bloco Cirúrgico para a UTI. O sistema centraliza a visualização do censo de leitos, automatiza o fluxo de solicitações de UTI vindas do Bloco Cirúrgico, monitora o tempo de transferência após a finalização da cirurgia por meio de um cronômetro de tempo de liberação e auxilia a UTI na alocação rápida das vagas disponíveis.

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

- **Painel de Leitos (Censo UTI):** Visualização em tempo real do estado de ocupação de cada leito, com informações completas do paciente, necessidade de isolamento e status. Permite à equipe da **UTI** determinar as vagas disponíveis para alocação.
- **Gerenciador de Solicitações:** Painel focado na **UTI** para gerenciar as solicitações de vagas pendentes vindas do Bloco Cirúrgico.
- **Definição de Prioridades:** Permite ao **Bloco Cirúrgico** definir o nível de prioridade (de **P1 a P10**) para cada paciente cirúrgico que aguarda leito.
- **Controle de Reservas e Conflitos:** Inteligência para evitar conflitos de reserva de leito (ex: não permitir novas reservas automáticas para leitos já ocupados ou reservados).
- **Tempo de Transferência:** Cronômetro dinâmico para acompanhar o tempo gasto na transferência do Bloco Cirúrgico para o leito de UTI (iniciado logo após a finalização da cirurgia).
- **Fluxo pós-alta da UTI:** O destino do paciente após a alta da UTI é de responsabilidade e determinação do **NIR (Núcleo Interno de Regulação)**.
- **Autenticação LDAP/Active Directory:** Login seguro integrado com o diretório ativo corporativo do hospital, além de fallback automático para desenvolvimento local.
- **Dashboard de Indicadores:** Métricas consolidadas sobre taxa de ocupação, tempo médio de espera, cancelamentos de reserva e fluxo de altas.

---

## ⚙️ Configurações de Ambiente (`.env.example`)

Os arquivos de configuração e exemplos de credenciais contidos em `.env.example` (como conexões com bancos PostgreSQL/Oracle e LDAP/AD) contêm apenas **endereços e credenciais de simulação/exemplo genéricos**. Os acessos reais à rede hospitalar de produção são configurados estritamente locais no servidor no arquivo `.env`, que é ignorado pelo Git (conforme configurado em `.gitignore`) garantindo total segurança do ambiente.

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

---

## 💾 Backups

A aplicação conta com dois mecanismos de backup para o banco de dados SQLite local (`app.db`):

### 1. Backup Preventivo (Automático no Deploy)
Durante a execução do script `scratch/git_pull_and_rebuild.py`, um backup a quente consistente é feito automaticamente antes de aplicar novas migrations e reiniciar os containers:
- Arquivo gerado: `/var/app/hc-uti-manager/data/backup_pre_deploy.db`

### 2. Backup Diário Rotativo (Cron Job na VM)
Existe um script em `scratch/backup_db.sh` preparado para rodar rotineiramente.

Para cadastrá-lo como cron diário no Linux do host da VM:
1. Acesse a VM via SSH.
2. Dê permissão de execução ao script:
   ```bash
   chmod +x /var/app/hc-uti-manager/scratch/backup_db.sh
   ```
3. Abra o agendador de tarefas cron do usuário root:
   ```bash
   crontab -e
   ```
4. Adicione a linha abaixo no final do arquivo para rodar o backup todos os dias às 02:00 da manhã (mantendo o histórico rotativo dos últimos 7 dias compactados em `.gz`):
   ```cron
   0 2 * * * /var/app/hc-uti-manager/scratch/backup_db.sh > /dev/null 2>&1
   ```
5. Salve e saia do editor.