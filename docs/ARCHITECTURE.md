# Arquitetura do Projeto

Este documento detalha a arquitetura em camadas e os padroes de projeto utilizados no framework, com foco em desacoplamento e flexibilidade.

## Arquitetura em Camadas

O fluxo de uma requisicao na aplicacao segue um padrao claro e unidirecional, garantindo a separacao de responsabilidades.

**Fluxo: `Roteador` -> `Controller` -> `Provedor`**

1.  **Roteador (`src/routers/`)**
    - **Responsabilidade:** Define os endpoints da API (`@router.get`, `@router.post`, etc.), valida os dados de entrada (usando Pydantic) e gerencia a injecao de dependencias.
    - **Funcao:** E o ponto de entrada de uma requisicao HTTP. Ele utiliza o sistema `Depends` do FastAPI para solicitar as dependencias necessarias (como um provedor de dados) e, em seguida, chama a funcao apropriada no controller, passando a dependencia ja resolvida.

2.  **Controller (`src/controllers/`)**
    - **Responsabilidade:** Contem a logica de negocio. Ele orquestra as operacoes, formata dados e toma decisoes.
    - **Funcao:** Recebe as dependencias ja prontas do roteador. Ele nao sabe (e nao deve saber) qual implementacao concreta esta sendo usada (ex: se os dados vem de um banco ou de um CSV). Ele apenas utiliza os metodos definidos pela interface do provedor.

3.  **Provedor (`src/providers/`)**
    - **Responsabilidade:** Camada de acesso a dados. E a unica parte do sistema que sabe como obter ou persistir dados em uma fonte especifica (PostgreSQL, Oracle, CSV, API externa, etc.).
    - **Funcao:** Implementa uma interface (contrato) definida em `src/providers/interfaces/`. Cada implementacao concreta (ex: `PacientePostgresProvider`, `PacienteCsvProvider`) contem a logica especifica para uma fonte de dados.

## Padrao de Injecao de Dependencias e Arquitetura de Dados

O sistema utiliza a injecao de dependencias do FastAPI para isolar o acesso a dados da logica de negocios, operando de forma hibrida com duas fontes de dados:

1. **Banco Hospitalar Oficial (AGHU - PostgreSQL):**
   - Utilizado para ler dados em tempo real do hospital, como cadastro de pacientes e agendamentos de cirurgias.
   - Provedores como `PacientePostgresProvider` e `LeitoAghuProvider` dependem da sessao `get_aghu_db_session` injetada pelo FastAPI.

2. **Banco Local do Sistema (SQLite - `app.db`):**
   - Utilizado para gravar e persistir dados e estados exclusivos do painel da UTI, como solicitacoes de vaga, estados locais de leito, historico de acoes e alertas.
   - Provedores como `SolicitacaoLeitoProvider` e `AlertaProvider` dependem da sessao `get_app_db_session`.

### Como Funciona a Injecao no Roteador

Os roteadores do FastAPI (`src/routers/`) declaram as interfaces dos provedores como dependencias usando `Depends()`. O framework resolve a implementacao concreta baseando-se no arquivo `src/dependencies.py`:

```python
# Em src/routers/paciente.py
@router.get("", response_model=List[dict])
async def listar_pacientes(
    provider: PacienteProviderInterface = Depends(get_paciente_provider)
):
    return await paciente_controller.listar_pacientes(provider)
```

E no arquivo `src/dependencies.py`, as dependencias de banco de dados sao resolvidas e injetadas automaticamente:

```python
# Em src/dependencies.py
def get_paciente_provider(
    session: AsyncSession = Depends(get_aghu_db_session)
) -> PacienteProviderInterface:
    return PacientePostgresProvider(session=session)
```

### Vantagens desta Abordagem

- **Desacoplamento Real:** A logica de negocio no controller nunca e afetada pela tecnologia ou infraestrutura de banco de dados.
- **Testabilidade:** Permite mockar facilmente as interfaces dos provedores para testes unitarios ou de integracao.
- **Eficiencia:** Conexoes com os respectivos bancos de dados (Postgres ou SQLite) so sao abertas se a rota executada realmente precisar do provedor correspondente.
