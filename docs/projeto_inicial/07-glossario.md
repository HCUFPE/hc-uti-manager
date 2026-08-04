# Glossário e Referências — HC-UTI Manager

Este documento define os principais termos técnicos e conceitos de negócio utilizados no sistema **HC-UTI Manager**, além de listar as fontes normativas e técnicas de referência.

---

## 1. Glossário de Termos e Siglas

*   **AGHU (Aplicativo de Gestão para Hospitais Universitários):** Sistema hospitalar oficial desenvolvido pela Ebserh. É a fonte primária de dados para pacientes, prontuários e agendamento de cirurgias.
*   **NIR (Núcleo Interno de Regulação):** Setor hospitalar responsável pelo gerenciamento de leitos, controle de altas, transferências internas e externas de pacientes no hospital.
*   **BC (Bloco Cirúrgico):** Setor onde ocorrem as cirurgias eletivas e de urgência, sendo o principal solicitante de leitos de UTI para o pós-operatório.
*   **Bed Cards (Cards de Leito):** Representação visual no painel eletrônico de cada leito físico da UTI, exibindo seu status operacional atual (ocupado, disponível, alta, higienização ou desativado).
*   **Troca de Paciente (Swap):** Regra de negócio na qual o Bloco Cirúrgico edita uma solicitação e substitui o prontuário do paciente por outro. O sistema faz a transferência automática da reserva física e inativa a solicitação anterior para evitar duplicidades na fila.
*   **Fila de Prioridades (P1 a P10):** Classificação dinâmica sequencial que determina a ordem de preferência para admissão na UTI, baseada na gravidade clínica e no horário da cirurgia programada.
*   **Status do Leito (Ciclo de Vida):**
    *   *Disponível:* Pronto para receber um novo paciente.
    *   *Ocupado:* Paciente internado fisicamente.
    *   *Alta:* Alta clínica concedida pelo médico da UTI, aguardando regulação do NIR para liberação física.
    *   *Higienização:* Período de limpeza do leito após a saída de um paciente.
    *   *Desativado:* Leito interditado por motivos técnicos, de manutenção ou clínicos.
*   **Status da Solicitação (Ciclo de Fila):**
    *   *Pendente:* Solicitação aguarda na fila por um leito livre.
    *   *Reservado:* Vínculo estabelecido entre a solicitação e um leito físico específico da UTI.
*   **LDAP / Active Directory (AD):** Protocolo e diretório corporativo da Ebserh usado para autenticação centralizada dos profissionais através de seu login de rede padrão.
*   **JWT (JSON Web Token):** Mecanismo de segurança de sessão que trafega assinado entre cliente e servidor para autenticar as chamadas de API.

---

## 2. Referências

*   **Manuais de Fluxo de Leitos do HC-UFPE:** Diretrizes locais que norteiam as atribuições da UTI, do Bloco Cirúrgico e da Regulação de Leitos (NIR).
*   **Regimento Interno do Núcleo Interno de Regulação (NIR) - Ebserh:** Regulamentação sobre a gestão de altas e transferências hospitalares.
*   **Lei Geral de Proteção de Dados (LGPD) — Lei nº 13.709/2018:** Diretrizes de segurança e rastreabilidade para o tratamento de dados pessoais sensíveis de saúde de pacientes.
*   **Documentações Técnicas do Repositório:**
    *   [FastAPI Documentation](https://fastapi.tiangolo.com)
    *   [SQLAlchemy Async ORM Guide](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
    *   [Vue.js 3 - Single Page Applications Guide](https://vuejs.org)
