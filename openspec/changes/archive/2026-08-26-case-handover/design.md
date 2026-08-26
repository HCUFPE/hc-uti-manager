## Context

Implantação da funcionalidade de Passagem de Caso clínica contendo um JSON estruturado com dados detalhados da cirurgia e do paciente pós-operatório (via aérea, suporte cardiovascular, balanço hídrico, acessos e dispositivos, intercorrências e profissional responsável).

## Goals / Non-Goals

**Goals:**
- Implementar o formulário estruturado de Passagem de Caso contendo todos os dados clínicos indicados no documento padrão.
- Validar no frontend e no backend a obrigatoriedade dos campos (Respiratório, Cardiovascular, Sangramento, Acessos/Feridas e Profissional Responsável).
- Permitir edição da passagem de caso pelo Bloco Cirúrgico antes da validação da UTI.
- Exibir a ação "Ver Passagem de Caso" permanentemente no leito da UTI.

## Decisions

### 1. Schema JSON para persistência (coluna `passagem_caso` no SQLite)

O campo `passagem_caso` (do tipo `TEXT`) conterá um documento JSON estruturado. Abaixo está a definição do modelo a ser persistido e enviado entre o frontend e backend:

```json
{
  "cirurgia_nao_realizada": false,
  "procedimento_realizado": "String (Obrigatório exceto se cirurgia_nao_realizada = true)",
  "anestesia": "String",
  "alergias": {
    "opcao": "Sim / Não",
    "detalhe": "String (Se Sim)"
  },
  "isolamento": "Não / Contato / Gotículas / Aerossóis (Obrigatório)",
  "respiratorio": {
    "via_aerea": {
      "espontanea": false,
      "tot": false,
      "traqueostomia": false,
      "outro": false,
      "outro_detalhe": "String (Se outro)"
    },
    "suporte": {
      "ar_ambiente": false,
      "o2_cateter": false,
      "mascara": false,
      "ventilacao_mecanica": false
    }
  },
  "cardiovascular": {
    "hemodinamica": "Estável / Instável",
    "drogas_vasoativas": {
      "opcao": "Não / Sim",
      "detalhe": "String (Se Sim)"
    },
    "reposicao_volemica": "Não / Sim",
    "transfusao": {
      "opcao": "Não / Sim",
      "detalhe": "String (Se Sim)"
    }
  },
  "sangramento_balanco": {
    "sangramento_estimado": "Mínimo / Pequeno / Moderado / Importante / Não se aplica",
    "sangramento_volume": "String/Number (Se Importante)",
    "diurese_intraoperatoria": {
      "opcao": "valor / Não se aplica",
      "valor": "String/Number"
    }
  },
  "acessos_dispositivos": {
    "acessos_venosos": {
      "periferico": false,
      "periferico_local": "String",
      "periferico_data": "String (Opcional - YYYY-MM-DD)",
      "cvc": false,
      "cvc_local": "String",
      "cvc_data": "String (Opcional - YYYY-MM-DD)",
      "picc": false,
      "picc_local": "String",
      "picc_data": "String (Opcional - YYYY-MM-DD)",
      "outro": false,
      "outro_detalhe": "String",
      "outro_data": "String (Opcional - YYYY-MM-DD)"
    },
    "pai": {
      "opcao": "Não / Sim",
      "local": "String"
    },
    "sonda_vesical": {
      "opcao": "Não / Sim",
      "n_sonda": "String"
    },
    "ferida_operatoria": {
      "local": "String",
      "nao_se_aplica": false
    },
    "drenos": {
      "opcao": "Não / Sim",
      "tipo_local": "String"
    },
    "outros": {
      "sng_sne": false,
      "ostomia": false,
      "outro": false,
      "outro_detalhe": "String"
    }
  },
  "medicamentos": {
    "antibiotico": {
      "opcao": "Não / Sim",
      "detalhe": "String (Se Sim)"
    },
    "outras_medicacoes": "String"
  },
  "intercorrencias": {
    "nao_houve": false,
    "hipotensao": false,
    "hipertensao": false,
    "arritmia": false,
    "dessaturacao": false,
    "broncoespasmo": false,
    "sangramento_importante": false,
    "reacao_medicamentosa": false,
    "parada_cardiorespiratoria": false,
    "dificil_via_aerea": false,
    "outro": false,
    "outro_detalhe": "String",
    "descricao_conduta": "String"
  },
  "profissional_responsavel": "String (Obrigatório)"
}
```

### 2. Fluxo de Edição da Passagem pelo Bloco Cirúrgico
* Rota: `PUT /api/solicitacoes/{id}/passagem-caso`
* Validação do Backend: Verifica se a solicitação está em estado finalizado de cirurgia mas **ainda não foi liberada/sinalizada como ciente pela UTI** (ou seja, `status` na tabela do banco ainda não mudou de `"Cirurgia Finalizada"` para `"Encaminhamento Liberado"` / `"Admitido"`). Se a UTI já tiver validado, retorna erro `403 Forbidden`.

### 3. Exibição Permanente na UTI
* O card do leito no frontend (`BedCard.vue`) passará a ter um link secundário ("Ver Passagem") que abre o modal da passagem de caso em modo somente leitura a qualquer momento, permitindo que a UTI consulte as intercorrências ou acessos mesmo após admitir o paciente.

### 4. Controle de Concorrência Atômica (SQLite)
* O backend utiliza instruções SQL de atualização condicional direta (`UPDATE ... WHERE cirurgia_finalizada = False/None` e `WHERE encaminhamento_liberado = False/None`) e validação via `rowcount` para garantir atomicidade sob concorrência. Disparos duplos paralelos de salvamento ou liberação geram respostas HTTP `409 Conflict` tratadas no frontend.

### 5. Visualização Retrospectiva no Histórico de Ações
* O histórico geral de ações de auditoria (`Historico.vue`) disponibilizará um botão amigável **"Ver Passagem"** para cada entrada de auditoria vinculada à cirurgia concluída ou à passagem criada. O frontend consome o novo endpoint `GET /api/solicitacoes/{id}` e exibe de forma limpa a ficha clínica, apresentando a mensagem de "Passagem de caso não cadastrada." para registros antigos onde a coluna esteja vazia no banco.
