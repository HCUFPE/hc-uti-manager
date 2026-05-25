## Context

Atualmente, o processo de criação de solicitações de leito exige a digitação manual de dados que já existem no sistema de prontuários e cirurgias do hospital (AGHU). A proposta é simplificar a entrada para os setores solicitantes (Bloco Cirúrgico, Centro Obstétrico e Hemodinâmica) integrando diretamente a pesquisa de prontuário com o banco de dados do AGHU.

## Goals / Non-Goals

**Goals:**
- Criar endpoint no backend para pesquisar cirurgia agendada no AGHU com base no prontuário do paciente.
- Modificar o modelo `SolicitacaoLeito` para persistir o nome do paciente e o procedimento cirúrgico retornado.
- Automatizar o preenchimento dos campos `idade` (calculada a partir da data de nascimento), `especialidade`, `procedimento`, `data_cirurgia` e `turno` (mapeado de acordo com a hora de início).
- Ajustar o frontend para expor um fluxo intuitivo: o usuário digita o prontuário, a tela exibe uma prévia com as informações recuperadas do AGHU para validação, e então permite salvar com a prioridade selecionada.

**Non-Goals:**
- Não serão feitas modificações na lógica de censo ou no controle de leitos físicos.
- Não será integrada a alteração retroativa das informações demográficas no AGHU (fluxo unidirecional de consulta).

## Decisions

### 1. Novo Endpoint e Integração de Banco
- Criaremos a rota `GET /api/solicitacoes/consultar-aghu/{prontuario}` no router `solicitacoes_leito.py`.
- O endpoint irá instanciar o `AghuCirurgiaProvider` passando a sessão assíncrona do PostgreSQL.
- O provider lerá o SQL em `src/providers/sql/solicitacao/obter_cirurgia_aghu.sql` contendo a consulta especificada pelo usuário.

### 2. Mapeamento de Horário de Início para Turno
No backend, o campo "Hora de Início" retornado pelo AGHU no formato `HH24:MI` será mapeado para o turno correspondente:
- **07:00 às 12:59**: "Manhã"
- **13:00 às 18:59**: "Tarde"
- **19:00 às 06:59**: "Noite"

### 3. Modelo e Colunas no SQLite
O modelo `SolicitacaoLeito` em `src/models/solicitacao_leito.py` será atualizado com os novos campos:
- `nome`: `Column(String(150), nullable=True)`
- `procedimento`: `Column(String(250), nullable=True)`
- `hora_cirurgia`: `Column(String(5), nullable=True)` -- Para armazenar a hora de início (HH:MM) e usar na ordenação

Como a aplicação recria o banco de dados local SQLite caso ele seja deletado (ou o Lifespan aplica o `create_all`), isso garante a atualização do banco em ambiente de testes. No entanto, para evitar perda de dados dos testes anteriores do usuário, forneceremos um comando SQL rápido ou script de migração no passo de implementação para atualizar o banco SQLite atual adicionando as novas colunas.

### 4. Fluxo no Frontend (UX)
Ao abrir o modal "Nova Solicitação":
1. Exibir apenas os campos **Prontuário** e **Prioridade** (esta última pode vir desabilitada ou oculta para criação inicial, já que é calculada de forma dinâmica).
2. Um botão ou gatilho ao preencher o prontuário fará a chamada à API `GET /api/solicitacoes/consultar-aghu/{prontuario}`.
3. Se encontrado, mostrar em destaque no modal os dados recuperados de forma somente leitura (Nome, Idade, Data/Hora da Cirurgia, Especialidade e Procedimento).
4. O botão "Salvar" só é habilitado após a consulta retornar sucesso.

### 5. Prioridade Inicial e Ordem de Exibição pelo Horário da Cirurgia
A prioridade inicial (P1, P2, P3...) e a exibição serão automatizadas com base no horário de início da cirurgia:
1. **Priorização Automática**: Ao criar/sincronizar o bucket de solicitações (mesma data e turno), o backend ordenará as solicitações pendentes de forma cronológica pela hora de início da cirurgia (`hora_cirurgia`). A cirurgia que iniciar mais cedo receberá automaticamente `P1`, a próxima `P2`, e assim sucessivamente.
2. **Ordenação na Exibição**: No frontend, o desempate na ordenação dentro do mesmo dia e turno será feito de forma crescente pelo horário da cirurgia (usando o campo `hora_cirurgia`), de modo que a fila exiba sempre as cirurgias agendadas mais cedo no topo.

## Risks / Trade-offs

- **[Risco]** Ausência de conexão com o AGHU em desenvolvimento/testes locais.
  - *Mitigação*: Se `POSTGRES_DSN` não estiver configurado ou ocorrer erro na conexão, o backend poderá cair em um fallback mockado (por exemplo, retornar dados fictícios baseados em prontuários conhecidos de teste como `77`, `123` e `1` para viabilizar testes offline).
- **[Risco]** Divergências de fuso horário ou formatos de data.
  - *Mitigação*: Utilizar manipulação rigorosa usando a biblioteca `datetime` do Python e garantindo a formatação em `DD-MM-YYYY` informada pelo usuário.
