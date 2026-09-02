## 1. Ajuste no Código Fonte Backend

- [x] 1.1 Atualizar `AlertaProvider.criar` em `src/providers/implementations/alerta_provider.py` para desduplicar alertas por título, prontuário e mensagem sem exigir igualdade estrita de timestamp.

## 2. Limpeza do Banco de Produção e Deploy

- [x] 2.1 Executar a remoção da duplicidade `#1018` na VM de Produção (`10.34.0.192`).
- [x] 2.2 Fazer o deploy do ajuste do backend para o ambiente de Produção.
