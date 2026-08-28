# Design: Melhorias na Regulação do NIR (Alerta de Admissão e Especialidade de Alta)

## Context

O HC UTI Manager atualmente gera alertas voltados para a UTI ou para o NIR. No entanto, as admissões concluídas (quando o paciente é fisicamente admitido no AGHU e sua reserva correspondente é finalizada) são registradas no histórico de ações, mas nenhum alerta explícito é enviado ao NIR. Adicionalmente, todos os alertas compartilham o mesmo estilo visual azul informativo no frontend e a mesma sinalização sonora periódica no background. O NIR precisa de uma forma de diferenciar as Admissões Concluídas visualmente e auditivamente.
Também é necessário facilitar o trabalho de triagem de altas exibindo a especialidade clínica do paciente de forma clara na tela de Solicitações de Alta.

## Goals / Non-Goals

**Objetivos (Goals):**
- Gerar automaticamente um alerta do tipo `admissao_concluida` para o NIR quando a admissão de uma reserva for concluída via sincronização de censo do AGHU.
- Renderizar esses alertas com um estilo visual verde/esmeralda de sucesso diferenciado no frontend.
- Reproduzir um padrão sonoro sintetizado diferente (melodia ascendente C-E-G com onda senoidal) para alertas de admissão concluída, em vez do bipe rápido padrão de 6 repetições.
- Exibir a especialidade do paciente diretamente na listagem de solicitações de alta no frontend (`Altas.vue`), consumindo a propriedade já existente retornada pela API.

**Não-Objetivos (Non-Goals):**
- Tocar sons para alertas já lidos ou arquivados.
- Utilizar arquivos físicos de som (MP3/WAV) para o som personalizado (usaremos síntese com a Web Audio API do navegador, mantendo o padrão do restante da aplicação para garantir portabilidade e evitar falhas de carregamento).

## Decisions

### 1. Gatilho de Geração de Alertas no Backend
- **Opção A**: Verificar diretamente na transação de banco de dados durante a atualização de status.
- **Opção B (Escolhida)**: Expandir a rotina `AlertaController._gerar_alerta_por_tipo` para processar eventos de histórico com tipo `conclusao` (que são gerados quando `alterou_admissao` é verdadeiro durante a sincronização inteligente do censo).
  - *Justificativa*: Se adequa perfeitamente à arquitetura atual de geração de alertas baseada no histórico de ações, mantendo as responsabilidades desacopladas.

### 2. Geração de Som Personalizado na Store de UI
- **Opção A**: Adicionar um arquivo de áudio físico (ex: `admissao.mp3`).
- **Opção B (Escolhida)**: Implementar uma nova função `tocarAlertaAdmissao()` no `uiStore` utilizando a Web Audio API com um oscilador do tipo `sine` (onda senoidal) tocando as notas dó, mi, sol ascendentes.
  - *Justificativa*: Evita consumo de rede adicional e problemas com links quebrados para arquivos de som, mantendo a geração de som 100% no lado do cliente e muito leve.

### 3. Estilização Visual na Tela de Alertas
- **Opção A**: Inserir estilos hardcoded na lista de alertas.
- **Opção B (Escolhida)**: Adicionar o mapeamento do tipo `admissao_concluida` no objeto de configuração `alertConfig` no arquivo `Alertas.vue`, importando o ícone `CheckCircleIcon` do Heroicons.
  - *Justificativa*: Mantém o padrão limpo de parametrização de componentes e reutilização de estilos da tela de alertas.

### 4. Priorização dos Alertas Sonoros
- **Opção A**: Priorizar o som de admissão sobre o som padrão.
- **Opção B (Escolhida)**: Priorizar o som de alerta padrão (6 bipes rápidos) sobre a melodia de admissão concluída.
  - *Justificativa*: Como os alertas padrão do sistema indicam urgência ou desvios críticos (ex: cancelamentos de alta, remoção de vagas do dia), eles devem reter maior atenção e sobrepor o som de admissão concluída (que é de natureza puramente informativa).

### 5. Exibição de Especialidade na Tela de Altas
- **Opção A**: Modificar a modelagem e salvar a especialidade na tabela de solicitações de alta.
- **Opção B (Escolhida)**: Utilizar a propriedade `especialidade` já retornada pela API `/api/altas` (mapeada a partir da especialidade atual do leito censo) e exibi-la de forma puramente visual no frontend.
  - *Justificativa*: A API do backend já resolve dinamicamente a especialidade a partir do estado censo enriquecido, dispensando alterações estruturais de tabelas no banco de dados e simplificando o escopo.

## Risks / Trade-offs

- **[Risco]** Políticas de autoplay de navegadores bloqueando a saída da Web Audio API.
  - *Mitigação*: O navegador já inicializa a saída de som a partir de qualquer clique de interação do usuário na página (como os botões de mute/unmute do menu), o que já contorna essa limitação no fluxo geral do app.
