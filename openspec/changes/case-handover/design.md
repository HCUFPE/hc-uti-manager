## Context

O sistema atual de regulação de leitos (HC-UTI Manager) realiza a transição de pacientes do Bloco Cirúrgico para a UTI através de um fluxo sequencial:
1. O solicitante finaliza a cirurgia (status `Cirurgia Finalizada`).
2. O painel da UTI destaca o leito correspondente em amarelo piscante e exibe o botão "Liberar Encaminhamento".
3. A equipe da UTI clica no botão, liberando o envio do paciente (status `Encaminhamento Liberado`).

Atualmente, não há campo para comunicação de dados clínicos relevantes de transição diretamente no sistema, forçando a equipe a fazer contato telefônico ou físico, o que pode atrasar a preparação do leito na UTI.

## Goals / Non-Goals

**Goals:**
- Permitir que a equipe cirúrgica grave opcionalmente observações críticas pós-operatórias (Passagem de Caso).
- Garantir que a equipe da UTI leia essas informações antes de clicar em "Liberar Encaminhamento".
- Manter o fluxo atual rápido e de um único clique para casos onde nenhuma informação de passagem de caso foi registrada.

**Non-Goals:**
- Tornar obrigatória a digitação de informações pelo Bloco Cirúrgico (a equipe cirúrgica tem tempo restrito e o preenchimento deve ser opcional).
- Alterar as regras médicas de admissão ou o painel de evolução clínica do paciente.

## Decisions

### 1. Modelo de Dados e Banco de Dados (SQLite & Alembic)
Adicionaremos a coluna `passagem_caso` do tipo `String` (opcional/nullable) na tabela `solicitacoes_leito`.
* **Alternativa considerada:** Criar uma tabela separada `passagem_casos`.
* **Razão da escolha:** Como a relação é de 1:1 com a solicitação de leito e as consultas serão simples leituras textuais, adicionar a coluna diretamente na tabela `solicitacoes_leito` simplifica o modelo de dados, otimiza o desempenho das queries e facilita a manutenção do banco SQLite.

### 2. Endpoints e Serialização da API
* **Gravação:** Ajustar a rota de finalização de cirurgia (`POST /api/solicitacoes/{id}/finalizar-cirurgia` ou similar) para aceitar um corpo de JSON com o campo opcional `passagem_caso`.
* **Leitura:** Na listagem de leitos do painel (`GET /api/leitos`), quando houver uma reserva ativa para o leito, o objeto do leito retornará os dados da reserva vinculada incluindo a nova string `passagem_caso`.

### 3. Componentização do Frontend (Vue 3)
* **Na fila do Bloco (Home.vue):** Ao clicar em "Finalizar Cirurgia", abriremos um modal com pergunta de duas opções ("Deseja preencher passagem de caso?"). A escolha "Sim" exibe uma caixa de texto (`textarea`). Ao salvar, enviamos os dados para a API.
* **No card do Leito (BedCard.vue):** O botão "Liberar Encaminhamento" interceptará o clique. Se o objeto da reserva do leito contiver `passagem_caso` preenchida, abriremos um modal de leitura obrigatória. A liberação só será disparada quando o usuário clicar em "Ciente e Liberar". Se a string estiver vazia, o fluxo original de 1 clique é disparado imediatamente.

## Risks / Trade-offs

- **[Risco]** A caixa de texto de passagem de caso se tornar muito burocrática e atrasar a finalização da cirurgia.
  - *Mitigação:* A janela de inserção começará com um fluxo binário muito rápido: o botão padrão de "Não" fecha a janela e conclui a cirurgia em um único clique sem exigir preenchimento.
