## Goals / Non-Goals

**Goals:**
- Armazenar o usuário (`lido_por`) e a data/hora (`lido_em`) no momento em que um alerta é marcado como lido.
- Exibir essas informações nos componentes de alerta no frontend.
- Garantir que a versão seja incrementada para `1.4.10`.
- Garantir retrocompatibilidade para que a rotina de detecção de duplicados (`_sincronizar_alertas`) não seja alterada e não gere alertas repetidos (já que `lido_em` e `lido_por` são colunas separadas e não interferem nas chaves de comparação de alertas).

## Decisions

### 1. Modelo `Alerta` (`src/models/alerta.py`)
- Adicionar as colunas:
  ```python
  lido_em = Column(DateTime, nullable=True)
  lido_por = Column(String(100), nullable=True)
  ```
- No método `to_dict()`, ajustar o fuso horário de `lido_em` para Brasília (-3h) e retornar:
  ```python
  "lido_em": lido_em_local.strftime("%d/%m/%Y %H:%M") if lido_em_local else None,
  "lido_por": self.lido_por
  ```

### 2. Rota `PUT /api/alertas/{alerta_id}/lido` (`src/routers/alertas.py`)
- Injetar a dependência `current_user: dict = Depends(auth_handler.decode_token)`.
- Passar o `current_user.get("username")` para o método do controller.

### 3. Controller `AlertaController` (`src/controllers/alerta_controller.py`)
- Atualizar a assinatura de `atualizar_status_leitura(self, alerta_id: int, lido: bool, username: str = None)`:
  - Se `lido` for `True`: `lido_em = datetime.utcnow()`, `lido_por = username`.
  - Se `lido` for `False`: `lido_em = None`, `lido_por = None`.
- Atualizar `marcar_todos_como_lidos(self, perfil: str, username: str = None)` para registrar as informações em lote.

### 4. Interface Frontend (`frontend/src/views/Alertas.vue` e `NotificationsPopover.vue`)
- Modificar o template para exibir a informação de leitura ao lado do ícone de relógio:
  ```html
  <span>Emitido em: {{ alerta.dataHora }}</span>
  <span v-if="alerta.lido && alerta.lido_em"> | Lido em: {{ alerta.lido_em }} ({{ alerta.lido_por }})</span>
  ```
