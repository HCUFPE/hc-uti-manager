## Context

O histórico de ações registra solicitações e cancelamentos de alta de leitos, mas falhava em persistir o campo `prontuario`, o que impedia a visualização integrada de todas as ações relacionadas a um paciente pelo seu número de prontuário. Além disso, a falta de bloqueio de concorrência/clique duplo no frontend permitia criar solicitações duplicadas no mesmo segundo para um único leito.

## Goals / Non-Goals

**Goals:**
- Desabilitar botões de envio no frontend durante a submissão de solicitações de alta.
- Buscar e persistir o número do prontuário do paciente nos eventos de histórico de solicitar, cancelar e concluir alta.

**Non-Goals:**
- Modificar o fluxo principal de aprovação de alta ou o censo do AGHU.

## Decisions

### 1. Registro de Prontuário no Histórico de Alta
- **Decisão**: Alterar os endpoints em `src/routers/altas.py` e `src/routers/leito.py` para extrair o prontuário do leito/solicitação antes de invocar `historico.registrar(..., prontuario=prontuario)`. Garantir que a rotina automática de conclusão de alta em `LeitosController` persista corretamente o prontuário.

### 2. Tratamento de Múltiplos Cliques no Modal de Alta do Frontend
- **Decisão**: Usar o estado de carregamento `submetendo` (ou similar) no modal de solicitar alta em `Solicitacoes.vue` para desabilitar o botão de confirmar (`:disabled="submetendo"`).
- **Risco**: Caso a requisição falhe, o botão deve voltar a ser habilitado.
- **Mitigação**: Executar a chamada à API dentro de um bloco `try...finally` garantindo que `submetendo.value = false` no final.

## Risks / Trade-offs

- **[Risco]**: A busca pelo prontuário pode falhar se o leito estiver desocupado no momento da chamada (ex: sincronização concorrente).
- **[Mitigação]**: Caso o prontuário não seja encontrado no censo, usar `"N/D"` como fallback seguro.
