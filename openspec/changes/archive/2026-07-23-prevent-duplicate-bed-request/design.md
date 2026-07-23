## Context

Atualmente, o `SolicitacaoLeitoController` faz validação de prontuário duplicado apenas contra as solicitações locais ativas (com status `Pendente` ou `Reservado`). Não há checagem contra o censo físico de leitos ativos da UTI obtido em tempo real através do AGHu (representado pelo `LeitoAghuProvider`).

## Goals / Non-Goals

**Goals:**
- Bloquear a criação de novas solicitações para prontuários que já estejam ocupando leitos fisicamente na UTI.
- Bloquear a alteração (edição) de prontuário de solicitações existentes caso o novo prontuário informado já ocupe leito fisicamente na UTI.
- Exibir uma mensagem clara com o identificador do leito ocupado pelo paciente.

**Non-Goals:**
- Não deve ser imposto nenhum bloqueio para pacientes que estejam de alta ou em outros setores do hospital que não sejam a UTI em questão.

## Decisions

### Injeção do Leito AGHU Provider na Controller de Solicitação de Leitos
Adicionar `census_provider: LeitoProviderInterface` ao construtor de `SolicitacaoLeitoController`.
- *Alternativa considerada:* Buscar diretamente a session do AGHu na controller. Rejeitado para manter o desacoplamento de infraestrutura e reusar o provedor existente.

### Local da Validação
A validação será realizada no backend dentro dos métodos `criar_solicitacao` e `editar_solicitacao` do `SolicitacaoLeitoController`.
- *Alternativa considerada:* Fazer a checagem no frontend. Rejeitado pois a API deve ser segura e consistente, e o frontend já trata erros 400 automaticamente exibindo o `detail` do erro no toast.

## Risks / Trade-offs

- **[Risco]** Lentidão ao carregar o censo durante a criação/edição.
  - *Mitigação:* O censo é uma query rápida indexada no PostgreSQL do AGHu, com impacto imperceptível.
