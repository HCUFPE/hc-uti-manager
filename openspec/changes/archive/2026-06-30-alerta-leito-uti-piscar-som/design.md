## Context

Atualmente, quando uma cirurgia é finalizada no Bloco Cirúrgico, o leito reservado correspondente no Painel de Leitos da UTI fica com fundo amarelo claro e borda amarela. No entanto, por ser um destaque estático, ele pode passar despercebido pela equipe da UTI, atrasando a liberação do encaminhamento.

## Goals / Non-Goals

**Goals:**
- Implementar uma animação piscante (pulsar de forma intermitente) nos cards de leito com status "Cirurgia Finalizada".
- Emitir um alerta sonoro de notificação quando uma cirurgia for sinalizada como finalizada.
- Restringir a animação visual e o sinal sonoro exclusivamente para usuários logados com perfil da UTI (ou administradores).
- Fornecer controle de ligar/desligar áudio no painel de leitos para respeitar o conforto do usuário.

**Non-Goals:**
- Tocar som em outros tipos de alerta que não sejam cirurgias finalizadas.
- Modificar o fluxo de estados do leito no backend ou a geração de alertas persistidos no banco de dados.

## Decisions

### 1. Animação de Piscar com CSS Customizado
- **Escolha**: Definir uma animação de keyframes CSS (`pulse-warning`) em `frontend/src/index.css`.
- **Alternativa considerada**: Usar a classe `animate-pulse` nativa do Tailwind.
- **Razão da Escolha**: O `animate-pulse` nativo do Tailwind diminui a opacidade do elemento inteiro (incluindo texto e botões internos), o que prejudica a legibilidade e a interação com os botões. Uma animação customizada focará em pulsar a cor de fundo, a borda e o sombreamento do card, mantendo o conteúdo perfeitamente legível.

### 2. Emissão de Áudio via Web Audio API
- **Escolha**: Usar a API nativa `AudioContext` do navegador para sintetizar um som de bipe duplo (duas frequências consecutivas) dinamicamente.
- **Alternativa considerada**: Carregar um arquivo estático `.mp3` ou `.wav` da pasta `/public`.
- **Razão da Escolha**: Evita requisições HTTP adicionais e problemas com caminhos de recursos em ambientes de produção containerizados. Além disso, garante compatibilidade total sem depender de formatos de decodificação de áudio que podem variar entre navegadores.

### 3. Detecção de Transição para Evitar Bip Repetitivo
- **Escolha**: Manter em `Home.vue` um conjunto (`Set`) de IDs de leitos que já estão com cirurgia finalizada. Ao buscar os leitos no polling, somente leitos que acabaram de entrar no estado "Cirurgia Finalizada" (não presentes no conjunto anterior) dispararão o alerta sonoro. Em seguida, atualizamos o conjunto.
- **Razão da Escolha**: Evita que o som toque a cada 2 minutos para o mesmo leito que a equipe já está ciente, reduzindo o ruído acústico no ambiente de trabalho.

## Risks / Trade-offs

- **[Risco] Bloqueio de Autoplay do Navegador** → Os navegadores modernos impedem a reprodução de áudio até que haja uma interação direta do usuário na página.
  - **Mitigação**: O som só será reproduzido após a primeira interação do usuário (clique no botão de som ou em qualquer lugar do painel). Adicionalmente, exibiremos o status "Som Ativado" / "Som Desativado" que necessita de clique do usuário, servindo como a interação requerida pelo navegador.
