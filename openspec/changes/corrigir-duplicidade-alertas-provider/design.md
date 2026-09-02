# Design de Implementação: Corrigir Duplicidade de Alertas

## Decisões Técnicas

### 1. Desduplicação Flexível no Provider (`alerta_provider.py`)
No arquivo `src/providers/implementations/alerta_provider.py`, atualizaremos o método `criar(data)` para a seguinte lógica:

```python
async def criar(self, data: dict) -> Alerta:
    stmt = select(Alerta).where(
        Alerta.titulo == data.get("titulo"),
        Alerta.prontuario == str(data.get("prontuario")),
        Alerta.mensagem == data.get("mensagem")
    )
    if data.get("perfil_alvo"):
        stmt = stmt.where(Alerta.perfil_alvo == data.get("perfil_alvo"))

    res = await self.session.execute(stmt)
    existentes = res.scalars().all()
    if existentes:
        return existentes[0]

    alerta = Alerta(**data)
    self.session.add(alerta)
    await self.session.commit()
    await self.session.refresh(alerta)
    return alerta
```

### 2. Rotina de Limpeza Única no Banco de Produção
Remover o alerta ID `#1018` através de um script de expurgo seguro que seleciona o menor ID por agrupamento de `titulo`, `prontuario` e `mensagem`.
