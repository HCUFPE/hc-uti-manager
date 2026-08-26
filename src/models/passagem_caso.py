from pydantic import BaseModel, Field, root_validator, validator
from typing import Optional, Dict, Any, Union

class AlergiasSchema(BaseModel):
    opcao: str # Sim / Não
    detalhe: Optional[str] = ""

    @validator("opcao", pre=True, always=True)
    def validate_opcao(cls, v):
        if v is None:
            return "Não"
        if v == "SIM":
            return "Sim"
        if v == "NÃO":
            return "Não"
        if v not in ["Sim", "Não"]:
            raise ValueError("Alergia deve ser 'Sim' ou 'Não'.")
        return v

    @root_validator(skip_on_failure=True)
    def validate_alergia(cls, values):
        opcao = values.get("opcao")
        detalhe = values.get("detalhe")
        if opcao == "Sim" and not (detalhe and detalhe.strip()):
            raise ValueError("O campo de detalhe da alergia é obrigatório quando selecionado Sim.")
        return values

class RespiratorioSchema(BaseModel):
    via_aerea: str # Espontânea / TOT / Traqueostomia / Outro
    via_aerea_outro_detalhe: Optional[str] = ""
    suporte: str # Ar ambiente / O2 cateter / Máscara / Ventilação mecânica

    @root_validator(skip_on_failure=True)
    def validate_respiratorio(cls, values):
        via = values.get("via_aerea")
        det = values.get("via_aerea_outro_detalhe")
        sup = values.get("suporte")
        if not via or not via.strip():
            raise ValueError("Via Aérea é obrigatória.")
        if via == "Outro" and not (det and det.strip()):
            raise ValueError("O detalhe da Via Aérea deve ser preenchido ao selecionar 'Outro'.")
        if not sup or not sup.strip():
            raise ValueError("Suporte Respiratório é obrigatório.")
        return values

class DrogasVasoativasSchema(BaseModel):
    opcao: str # Não / Sim
    detalhe: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_drogas(cls, values):
        opcao = values.get("opcao")
        detalhe = values.get("detalhe")
        if opcao == "Sim" and not (detalhe and detalhe.strip()):
            raise ValueError("O campo de droga/vazão é obrigatório quando drogas vasoativas estiver como 'Sim'.")
        return values

class TransfusaoSchema(BaseModel):
    opcao: str # Não / Sim
    detalhe: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_transfusao(cls, values):
        opcao = values.get("opcao")
        detalhe = values.get("detalhe")
        if opcao == "Sim" and not (detalhe and detalhe.strip()):
            raise ValueError("O campo de hemocomponente/quantidade é obrigatório quando transfusão estiver como 'Sim'.")
        return values

class CardiovascularSchema(BaseModel):
    hemodinamica: str # Estável / Instável
    drogas_vasoativas: DrogasVasoativasSchema
    reposicao_volemica: str # Não / Sim
    transfusao: TransfusaoSchema

    @validator("hemodinamica")
    def validate_hemo(cls, v):
        if v not in ["Estável", "Instável"]:
            raise ValueError("Hemodinâmica deve ser 'Estável' ou 'Instável'.")
        return v

    @validator("reposicao_volemica")
    def validate_reposicao(cls, v):
        if v not in ["Não", "Sim"]:
            raise ValueError("Reposição volêmica deve ser 'Não' ou 'Sim'.")
        return v

class DiureseSchema(BaseModel):
    opcao: str # valor / Não se aplica
    valor: Optional[Union[str, int, float]] = None

    @root_validator(skip_on_failure=True)
    def validate_diurese(cls, values):
        opcao = values.get("opcao")
        valor = values.get("valor")
        if opcao == "valor" and (valor is None or str(valor).strip() == ""):
            raise ValueError("O volume da Diurese é obrigatório.")
        return values

class SangramentoBalancoSchema(BaseModel):
    sangramento_estimado: str # Mínimo / Pequeno / Moderado / Importante / Não se aplica
    sangramento_volume: Optional[Union[str, int, float]] = None
    diurese_intraoperatoria: DiureseSchema

    @root_validator(skip_on_failure=True)
    def validate_sangramento(cls, values):
        est = values.get("sangramento_estimado")
        vol = values.get("sangramento_volume")
        if est == "Importante" and (vol is None or str(vol).strip() == ""):
            raise ValueError("O volume estimado de sangramento é obrigatório quando selecionado 'Importante'.")
        return values

class AcessosVenososSchema(BaseModel):
    periferico: bool = False
    periferico_local: Optional[str] = ""
    periferico_data: Optional[str] = ""
    cvc: bool = False
    cvc_local: Optional[str] = ""
    cvc_data: Optional[str] = ""
    picc: bool = False
    picc_local: Optional[str] = ""
    picc_data: Optional[str] = ""
    outro: bool = False
    outro_detalhe: Optional[str] = ""
    outro_data: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_acessos(cls, values):
        has_any = any([
            values.get("periferico"), values.get("cvc"), values.get("picc"), values.get("outro")
        ])
        if not has_any:
            raise ValueError("Ao menos um acesso venoso deve ser selecionado.")
        
        if values.get("periferico") and not (values.get("periferico_local") and values.get("periferico_local").strip()):
            raise ValueError("Local do Acesso Periférico é obrigatório.")
        if values.get("cvc") and not (values.get("cvc_local") and values.get("cvc_local").strip()):
            raise ValueError("Local do CVC é obrigatório.")
        if values.get("picc") and not (values.get("picc_local") and values.get("picc_local").strip()):
            raise ValueError("Local do PICC é obrigatório.")
        if values.get("outro") and not (values.get("outro_detalhe") and values.get("outro_detalhe").strip()):
            raise ValueError("Descrição e local do outro acesso é obrigatório.")
        return values

class PAI_Schema(BaseModel):
    opcao: str # Não / Sim
    local: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_pai(cls, values):
        if values.get("opcao") == "Sim" and not (values.get("local") and values.get("local").strip()):
            raise ValueError("Local do PAI é obrigatório quando marcado 'Sim'.")
        return values

class SondaVesicalSchema(BaseModel):
    opcao: str # Não / Sim
    n_sonda: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_sonda(cls, values):
        if values.get("opcao") == "Sim" and not (values.get("n_sonda") and values.get("n_sonda").strip()):
            raise ValueError("Número da Sonda Vesical é obrigatório quando marcado 'Sim'.")
        return values

class FeridaOperatoriaSchema(BaseModel):
    local: Optional[str] = ""
    nao_se_aplica: bool = False

    @root_validator(skip_on_failure=True)
    def validate_ferida(cls, values):
        if not values.get("nao_se_aplica") and not (values.get("local") and values.get("local").strip()):
            raise ValueError("Local da Ferida Operatória é obrigatório (ou marcar 'Não se aplica').")
        return values

class DrenosSchema(BaseModel):
    opcao: str # Não / Sim
    tipo_local: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_drenos(cls, values):
        if values.get("opcao") == "Sim" and not (values.get("tipo_local") and values.get("tipo_local").strip()):
            raise ValueError("Tipo/local do dreno é obrigatório quando marcado 'Sim'.")
        return values

class OutrosDispositivosSchema(BaseModel):
    sng_sne: bool = False
    ostomia: bool = False
    outro: bool = False
    outro_detalhe: Optional[str] = ""

class AcessosDispositivosSchema(BaseModel):
    acessos_venosos: AcessosVenososSchema
    pai: PAI_Schema
    sonda_vesical: SondaVesicalSchema
    ferida_operatoria: FeridaOperatoriaSchema
    drenos: DrenosSchema
    outros: Optional[OutrosDispositivosSchema] = None

class AntibioticoSchema(BaseModel):
    opcao: str # Não / Sim
    detalhe: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_antibiotico(cls, values):
        if values.get("opcao") == "Sim" and not (values.get("detalhe") and values.get("detalhe").strip()):
            raise ValueError("Qual/horário do antibiótico é obrigatório quando marcado 'Sim'.")
        return values

class MedicamentosSchema(BaseModel):
    antibiotico: AntibioticoSchema
    outras_medicacoes: Optional[str] = ""

class IntercorrenciasSchema(BaseModel):
    nao_houve: bool = False
    hipotensao: bool = False
    hipertensao: bool = False
    arritmia: bool = False
    dessaturacao: bool = False
    broncoespasmo: bool = False
    sangramento_importante: bool = False
    reacao_medicamentosa: bool = False
    parada_cardiorespiratoria: bool = False
    dificil_via_aerea: bool = False
    outro: bool = False
    outro_detalhe: Optional[str] = ""
    descricao_conduta: Optional[str] = ""

    @root_validator(skip_on_failure=True)
    def validate_intercorrencias(cls, values):
        fields = [
            values.get("nao_houve"), values.get("hipotensao"), values.get("hipertensao"),
            values.get("arritmia"), values.get("dessaturacao"), values.get("broncoespasmo"),
            values.get("sangramento_importante"), values.get("reacao_medicamentosa"),
            values.get("parada_cardiorespiratoria"), values.get("dificil_via_aerea"),
            values.get("outro")
        ]
        if not any(fields):
            raise ValueError("Ao menos uma opção de intercorrência deve ser selecionada (ou 'Não houve').")
        if values.get("outro") and not (values.get("outro_detalhe") and values.get("outro_detalhe").strip()):
            raise ValueError("O detalhe de 'Outro' em intercorrências deve ser preenchido.")
        return values

class PassagemCasoSchema(BaseModel):
    cirurgia_nao_realizada: bool = False
    procedimento_realizado: Optional[str] = ""
    anestesia: Optional[str] = ""
    alergias: AlergiasSchema
    isolamento: Optional[str] = "Não"
    respiratorio: RespiratorioSchema
    cardiovascular: CardiovascularSchema
    sangramento_balanco: SangramentoBalancoSchema
    acessos_dispositivos: AcessosDispositivosSchema
    medicamentos: MedicamentosSchema
    intercorrencias: IntercorrenciasSchema
    profissional_responsavel: str

    @root_validator(skip_on_failure=True)
    def validate_procedimento(cls, values):
        nao_realizada = values.get("cirurgia_nao_realizada")
        proc = values.get("procedimento_realizado")
        if not nao_realizada and not (proc and proc.strip()):
            raise ValueError("Procedimento realizado é obrigatório (exceto se a cirurgia não tiver sido realizada).")
        return values

    @validator("anestesia")
    def validate_anestesia(cls, v):
        if not v or not v.strip():
            raise ValueError("Anestesia é obrigatória.")
        return v

    @validator("isolamento", pre=True, always=True)
    def validate_isolamento(cls, v):
        if v is None:
            return "Não"
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("O campo Isolamento é obrigatório.")
        if v not in ["Não", "Contato", "Gotículas", "Aerossóis"]:
            raise ValueError("Isolamento deve ser 'Não', 'Contato', 'Gotículas' ou 'Aerossóis'.")
        return v

    @validator("profissional_responsavel")
    def validate_profissional(cls, v):
        if not v or not v.strip():
            raise ValueError("Profissional responsável pela passagem é obrigatório.")
        return v
