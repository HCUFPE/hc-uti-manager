# Modelo de Dados e Dicionário — HC-UTI Manager

Este documento descreve o modelo físico e lógico dos dados armazenados no banco de dados SQLite local (`app.db`) e o dicionário de campos utilizados na integração com o AGHU.

---

## 1. Modelo Entidade-Relacionamento (ERD)

```mermaid
erDiagram
    solicitacoes_leito ||--o| leito_estados : "vincula reserva (1:1)"
    solicitacoes_leito ||--o{ historico_acoes : "gera log"
    solicitacoes_leito ||--o{ alertas : "gera notificacao"
    
    solicitacoes_leito {
        int id PK
        string prontuario "NOT NULL"
        string nome
        int idade
        string especialidade "NOT NULL"
        string procedimento
        string tipo "NOT NULL"
        string status "NOT NULL (Pendente/Reservado)"
        string turno "NOT NULL"
        string data_cirurgia
        string hora_cirurgia
        string destino
        string prioridade
        boolean prioridade_manual "NOT NULL"
        string perfil_solicitante
        boolean cirurgia_finalizada "NOT NULL"
        boolean encaminhamento_liberado "NOT NULL"
        datetime criado_em
        datetime atualizado_em
    }
    
    leito_estados {
        string lto_id PK
        boolean alta_solicitada "NOT NULL"
        int prontuario_proximo
        int idade_proximo
        string especialidade_proximo
        int solicitacao_id FK
        datetime atualizado_em
    }
    
    historico_acoes {
        int id PK
        string operador "NOT NULL"
        string tipo "NOT NULL (badge color)"
        string acao "NOT NULL (resumo)"
        string detalhes "NOT NULL"
        string prontuario
        datetime criado_em
    }
    
    alertas {
        int id PK
        string tipo "NOT NULL (critico/aviso/info)"
        string titulo "NOT NULL"
        string mensagem "NOT NULL"
        string prontuario
        boolean lido "NOT NULL"
        string lido_por
        datetime criado_em
    }
```

---

## 2. Dicionário de Dados (Principais Tabelas)

### A. Tabela `solicitacoes_leito`
Armazena a fila de solicitações de vagas pós-operatórias ou reguladas para a UTI.

*   `id` (INTEGER, PK, Autoincrement): Chave primária.
*   `prontuario` (VARCHAR(50)): Identificador único do prontuário do paciente no AGHU.
*   `nome` (VARCHAR(150)): Nome completo do paciente.
*   `idade` (INTEGER): Idade do paciente no momento da solicitação.
*   `especialidade` (VARCHAR(100)): Especialidade médica responsável (ex: Cardiologia).
*   `procedimento` (VARCHAR(250)): Nome do procedimento cirúrgico.
*   `tipo` (VARCHAR(50)): Tipo de leito solicitado (ex: Cirurgico, HEM, Obstetrico).
*   `status` (VARCHAR(50)): Estado da solicitação (`Pendente`, `Reservado`).
*   `turno` (VARCHAR(50)): Turno da cirurgia (`Manha`, `Tarde`, `Noite`).
*   `prioridade` (VARCHAR(10)): Rank sequencial na fila (ex: `P1`, `P2`, ...).
*   `prioridade_manual` (BOOLEAN): Define se a prioridade foi fixada manualmente pelo operador.

### B. Tabela `leito_estados`
Gere o estado e vínculos extras dos leitos físicos da UTI que não existem no AGHU.

*   `lto_id` (VARCHAR(14), PK): Nome identificador do leito físico (ex: `Leito 05`).
*   `alta_solicitada` (BOOLEAN): Se a UTI solicitou alta deste leito para o NIR regular.
*   `prontuario_proximo` (INTEGER): Prontuário do paciente reservado para este leito.
*   `solicitacao_id` (INTEGER, FK): Referência da solicitação que possui a reserva ativa.

---

## 3. Schema JSON de Validação (Criação de Solicitação)

Schema utilizado pelas APIs do backend para validação das requisições recebidas via frontend:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SolicitacaoLeitoPayload",
  "type": "object",
  "properties": {
    "prontuario": { 
      "type": "string", 
      "pattern": "^[0-9]+$",
      "description": "Prontuário numérico do paciente cadastrado no AGHU"
    },
    "tipo": { 
      "type": "string", 
      "enum": ["Cirurgico", "HEM", "Obstetrico", "UTI", "Outro"] 
    },
    "prioridade": { 
      "type": ["string", "null"],
      "pattern": "^P[0-9]+$"
    },
    "perfil_solicitante": { 
      "type": "string",
      "enum": ["BC", "COB", "HEM", "UTI", "NIR", "Administrador"]
    }
  },
  "required": ["prontuario", "tipo", "perfil_solicitante"]
}
```

---

## 4. Regras de Integridade de Dados

*   **Não-Duplicidade de Fila:** Um paciente com prontuário ativo em status `Pendente` ou `Reservado` não pode ter uma segunda solicitação aberta no sistema.
*   **Vínculo Unívoco de Reserva:** Cada leito físico só pode ter uma única reserva ativa (`solicitacao_id` único no `leito_estados`).
*   **Auditoria Inalterável (Append-Only):** A tabela `historico_acoes` não aceita comandos de `UPDATE` ou `DELETE` em nível de aplicação. Todo evento gera um novo registro.
*   **Concorrência Travada:** A tabela de `alertas` só é alimentada por transações controladas via `asyncio.Lock` contra chamadas simultâneas de microsssegundos.
