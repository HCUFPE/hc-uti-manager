## Context

O sistema atual de regulação de leitos (HC-UTI Manager) realiza a transição de pacientes do Bloco Cirúrgico para a UTI através de um fluxo sequencial:
1. O solicitante finaliza a cirurgia (status `Cirurgia Finalizada`).
2. O painel da UTI destaca o leito correspondente em amarelo piscante e exibe o botão "Liberar Encaminhamento".
3. A equipe da UTI clica no botão, liberando o envio do paciente (status `Encaminhamento Liberado`).

Atualmente, não há campo para comunicação de dados clínicos relevantes de transição diretamente no sistema, forçando a equipe a fazer contato telefônico ou físico, o que pode atrasar a preparação do leito na UTI.

## Goals / Non-Goals

**Goals:**
- Permitir que a equipe cirúrgica grave obrigatoriamente observações clínicas críticas pós-operatórias (Passagem de Caso).
- Garantir que a equipe da UTI leia essas informações antes de clicar em "Liberar Encaminhamento".

**Non-Goals:**
- Alterar as regras médicas de admissão ou o painel de evolução clínica do paciente.

## Decisions

### 1. Modelo de Dados e Banco de Dados (SQLite & Alembic)
Adicionaremos a coluna `passagem_caso` do tipo `String` na tabela `solicitacoes_leito`.
* **Alternativa considerada:** Criar uma tabela separada `passagem_casos`.
* **Razão da escolha:** Como a relação é de 1:1 com a solicitação de leito e as consultas serão simples leituras textuais, adicionar a coluna diretamente na tabela `solicitacoes_leito` simplifica o modelo de dados, otimiza o desempenho das queries e facilita a manutenção do banco SQLite.

### 2. Endpoints e Serialização da API
* **Gravação:** Ajustar a rota de finalização de cirurgia (`POST /api/solicitacoes/{id}/finalizar-cirurgia` ou similar) para exigir um corpo de JSON com o campo obrigatório `passagem_caso`.
* **Leitura:** Na listagem de leitos do painel (`GET /api/leitos`), quando houver uma reserva ativa para o leito, o objeto do leito retornará os dados da reserva vinculada incluindo a nova string `passagem_caso`.

### 3. Componentização do Frontend (Vue 3)
* **Na fila do Bloco (Home.vue):** Ao clicar em "Finalizar Cirurgia", abriremos o modal obrigatório de passagem de caso contendo uma caixa de texto (`textarea`). O botão de "Salvar e Finalizar" permanece desabilitado enquanto a área de texto estiver vazia.
* **No card do Leito (BedCard.vue):** O botão "Liberar Encaminhamento" interceptará o clique abrindo obrigatoriamente um modal de leitura e checkpoint. A liberação só será disparada quando o usuário da UTI clicar em "Ciente e Liberar".

## Risks / Trade-offs

- **[Risco]** A caixa de texto de passagem de caso se tornar muito burocrática e atrasar a finalização da cirurgia.
  - *Mitigação:* A caixa de texto possui placeholders detalhados e curtos instruindo o preenchimento apenas dos parâmetros críticos do plantão (como DVA e ventilação).
