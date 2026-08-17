# Interfaces e Integrações — HC-UTI Manager

Este documento especifica as interfaces com o usuário (telas/fluxos), a interação com periféricos de hardware e os contratos de integração de software (APIs e Provedores) do sistema.

---

## 1. Interfaces com o Usuário (Telas e Componentes)

O frontend foi desenvolvido utilizando Vue.js com estilização moderna e responsiva, dividindo-se em quatro interfaces principais:

*   **Painel de Censo (Bed Card Board):** Painel mestre de visualização que organiza os leitos da UTI em um grid de cards interativos. Cada card muda de cor de acordo com o estado do leito físico (`Disponivel` - cinza/azul sutil, `Ocupado` - vermelho/rosa clínico, `Alta` - verde suave, `Higienizacao` - amarelo suave, `Desativado` - cinza escuro).
*   **Fila de Solicitações (Solicitantes):** Interface em tabela que lista as cirurgias do dia e solicitações ativas, mostrando prioridades (`P1` a `P10`), turnos e botões de ação dinâmica (Reservar, Editar via troca de paciente e Cancelar).
*   **Painel NIR (Altas e Transferências):** Painel exclusivo para o Núcleo Interno de Regulação definir a enfermaria ou leito de destino de pacientes que receberam alta clínica da UTI.
*   **Histórico de Ações (Auditoria):** Tela de consulta que exibe os logs de auditoria formatados por badges de cores dependendo do tipo de ação (solicitação, reserva, cancelamento, swap).

---

## 2. Integração de Hardware

Embora o sistema seja um aplicativo web executado no navegador, ele suporta a integração com **leitores de código de barras USB/Bluetooth** em modo emulação de teclado:
*   **Finalidade:** Permitir que o operador da UTI ou Bloco Cirúrgico bip a pulseira com código de barras do paciente ou o prontuário físico diretamente no campo de pesquisa ou no campo de criação de solicitações.
*   **Funcionamento:** O leitor decodifica o código e digita o número do prontuário no campo de entrada ativa, agilizando a busca automática e a importação de dados clínicos sem risco de erro de digitação.

---

## 3. Integração de Software (Contratos de Provedores)

A arquitetura do backend em Python (FastAPI) utiliza injeção de dependências para isolar as integrações de sistemas de terceiros (AD e AGHU):

### A. Contrato de Integração com o AGHU (PostgreSQL)
Mapeia a busca de cirurgias programadas diretamente no banco oficial do hospital:

```python
# Em src/providers/interfaces/aghu_cirurgia_provider_interface.py
class AghuCirurgiaProviderInterface:
    async def obter_cirurgia_por_prontuario(self, prontuario: str) -> dict:
        """
        Consulta o banco PostgreSQL do AGHU para retornar dados da cirurgia.
        Retorna: {
            "Prontuário": int,
            "Nome Completo": str,
            "Data de Nascimento": str,
            "Data da Cirurgia": str (DD-MM-YYYY),
            "Hora de Início": str (HH:MM),
            "Especialidade": str,
            "Procedimento Principal": str
        }
        """
        pass
```

### B. Contrato de Autenticação LDAP (Active Directory)
Verifica as credenciais do operador na rede corporativa e valida se ele pertence ao grupo de administradores:

```python
# Em src/auth/auth.py (Lógica interna do AuthHandler)
class LDAPAuthenticator:
    def autenticar_usuario(self, username: str, password: str) -> dict | None:
        """
        Conecta ao AD via ldap3, autentica a credencial e extrai os metadados do usuário.
        Verifica a presença no grupo 'GLO-SEC-HCPE-SETISD' para atribuir o cargo de Admin.
        Retorna: {
            "username": str,
            "nome_completo": str,
            "email": str,
            "is_admin": bool
        } se válido, ou None se inválido.
        """
        pass
```

### C. Contrato de Estado do Leito (SQLite Local)
Mantém o estado sincronizado de reservas e solicitações ativas localmente:

```python
# Em src/providers/implementations/leito_estado_provider.py
class LeitoEstadoProvider:
    async def salvar_reserva(self, lto_id: str, prontuario: int, idade: int, especialidade: str, solicitacao_id: int) -> bool:
        """Grava no SQLite a reserva física vinculada a uma solicitação ativa."""
        pass

    async def limpar_reserva_por_solicitacao(self, solicitacao_id: int) -> bool:
        """Libera o leito fisicamente no SQLite e limpa os campos de reserva."""
        pass

    async def bloquear_leito_clinico(self, lto_id: str) -> bool:
        """Define a flag bloqueado_clinico = True no banco SQLite local."""
        pass

    async def cancelar_bloqueio_clinico(self, lto_id: str) -> bool:
        """Define a flag bloqueado_clinico = False no banco SQLite local."""
        pass
```

### D. Endpoints REST da API (Reserva Preventiva)
*   `POST /api/leitos/{lto_id}/bloquear-clinico` — Ativa o bloqueio preventivo para o leito correspondente e registra log no histórico de auditoria.
*   `POST /api/leitos/{lto_id}/cancelar-reserva-clinica` — Remove o bloqueio preventivo do leito correspondente e registra o log de cancelamento.

