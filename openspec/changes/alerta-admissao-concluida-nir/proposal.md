# Proposta: Melhorias na Regulação do NIR (Alerta de Admissão e Especialidade de Alta)

## Why

Atualmente, quando a admissão de um paciente é concluída (o paciente é fisicamente admitido no leito da UTI conforme detectado pela sincronização do censo do AGHU), não há nenhuma notificação específica direcionada para o NIR (Núcleo Interno de Regulação). O NIR precisa ser notificado ativamente quando essas admissões são concluídas para rastrear a disponibilidade e o fluxo de leitos em tempo real. Esta notificação necessita de um tratamento visual (cor/estilo) e padrão sonoro diferentes para se diferenciar dos demais alertas tradicionais.
Além disso, a equipe do NIR precisa visualizar prontamente a especialidade médica responsável por cada paciente na lista de solicitações de alta para facilitar as tomadas de decisão e encaminhamento para os leitos de destino adequados.

## What Changes

- **Novo Tipo de Alerta**: Introduzir um novo tipo de alerta para Admissões Concluídas voltado para o NIR.
- **Estilo Visual Diferenciado**: Apresentar os alertas de admissão concluída com uma cor/estilo distintos na interface para diferenciá-los dos alertas comuns.
- **Alerta Sonoro Diferenciado**: Reproduzir um tom/melodia sonora diferente para os alertas de admissão concluída em comparação aos alertas sonoros comuns.
- **Gatilho no Backend**: Detectar quando um paciente que possuía reserva, cirurgia finalizada e encaminhamento liberado é finalmente admitido no AGHU (fluxo já realizado de forma automática pelo censo) e gerar este alerta específico.
- **Especialidade na Tela de Altas**: Exibir a especialidade do paciente como uma badge cinza ao lado da data/hora da solicitação na tela de solicitações de alta (`Altas.vue`), para facilitar a identificação da equipe responsável pelo NIR.

## Capabilities

### New Capabilities
<!-- Nenhuma nova funcionalidade está sendo introduzida, estamos modificando o comportamento dos alertas existentes -->

### Modified Capabilities
- `alertas`: Adicionar requisitos para alertas de admissão concluída voltados ao NIR, incluindo estilos visuais específicos, reprodução de alerta sonoro diferenciado e a geração automática destes alertas durante a conclusão de admissão via sincronização de censo.
- `solicitacao-leitos`: Adicionar requisito para exibição da especialidade médica do paciente na listagem de solicitações de alta na tela `Altas.vue`.

## Impact

- **Backend**: `AlertaController` e `SolicitacaoLeitoProvider` para capturar o evento de conclusão de admissão e gerar o alerta específico para o NIR.
- **Frontend**: `DefaultLayout.vue` e `uiStore` para gerenciar a nova melodia/tom sonoro e estilos diferentes na listagem de alertas; `Altas.vue` para exibir a badge de especialidade.
- **Banco de Dados**: Nenhuma alteração estrutural necessária (utilizaremos novos valores nos campos `tipo` ou `categoria` da tabela de alertas já existente).
