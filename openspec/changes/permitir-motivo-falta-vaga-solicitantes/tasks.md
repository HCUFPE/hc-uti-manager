# Tasks: Permitir Motivo "Falta de vaga de UTI" para Solicitantes

## 1. Frontend - Exibição do Motivo para Solicitantes

- [x] 1.1 Em `frontend/src/views/Solicitacoes.vue`, adicionar `'Falta de vaga de UTI'` à constante `MOTIVOS_CANCELAMENTO` e verificar que o array contém a opção.
- [x] 1.2 Em `frontend/src/views/Solicitacoes.vue`, atualizar a propriedade computada `motivosAtuais` para retornar `MOTIVOS_CANCELAMENTO` para solicitantes e administradores, preservando o retorno de `MOTIVOS_CANCELAMENTO_RESERVA` em cancelamento de reserva física e `['Falta de vaga de UTI', 'Paciente já ocupa um leito na UTI']` para perfil UTI puro.
- [x] 1.3 Validar a tipagem e compilação do frontend executando `npm run build` no diretório `frontend`.

## 2. Documentação e Governança

- [x] 2.1 Atualizar o caderno de requisitos funcionais em `docs/projeto_inicial/02-requisitos.md` refletindo a autorização do motivo "Falta de vaga de UTI" para solicitantes.
- [x] 2.2 Atualizar os fluxos de casos de uso em `docs/projeto_inicial/03-casos-uso.md` para documentar a opção nos fluxos do Bloco Cirúrgico, COB e Hemodinâmica.
- [x] 2.3 Atualizar `CHANGELOG.md` na seção `[1.8.0]` registrando a disponibilização do motivo de cancelamento para todos os setores solicitantes.
