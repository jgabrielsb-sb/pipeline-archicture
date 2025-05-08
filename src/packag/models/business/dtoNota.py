from pydantic import (
    BaseModel,
    model_validator
)
from typing import Optional

from datetime import date

from .enum import (
    EstadoEnum,
    MunicipioEnum
)


class NotaExtractedInfo(BaseModel):
    
    
    numero_nfs: str # numero
    codigo_autenticidade: str
    
    data_competencia: str 
    
    valor_liquido: str
    valor_total: str 
    valor_deducoes: str 
    valor_pis: str
    valor_cofins: str
    valor_inss: str
    valor_irrf: str
    valor_csll: str
    valor_issqn: str
    base_calculo: str
    aliquota: str
    issqn_a_reter: str
    
    estado: str
    
    codigo_tributacao: str 
    discriminacao_servico: str
    opt_simples_nacional: str
    
    serie: Optional[str] = None    
    nfse_substituida: Optional[str] = None 
    valor_outras_retencoes: Optional[str] = None
    data_emissao: Optional[str] = None
    
    atv_economica: str
    municipio: str
    
class NotaFormattedInfo(BaseModel):
    
    numero_nfs: str
    codigo_autenticidade: str
    
    data_competencia: str
    
    valor_liquido: str
    valor_total: str 
    valor_deducoes: str 
    valor_pis: str
    valor_cofins: str
    valor_inss: str
    valor_irrf: str
    valor_csll: str
    valor_issqn: str
    base_calculo: str
    aliquota: str
    issqn_a_reter: str
    
    estado: str
    
    codigo_tributacao: str 
    discriminacao_servico: str
    opt_simples_nacional: str
    
    serie: Optional[str] = None    
    nfse_substituida: Optional[str] = None 
    valor_outras_retencoes: Optional[str] = None
    data_emissao: Optional[str] = None
    
    atv_economica: str
    atv_economica_normalized: str
    municipio: str
    
    @model_validator(mode='after')   # must have only numbers in the following fields: cnpj, cpf, inscricao_municipal, cep, telefone
    def only_numbers(cls, values):
        only_numbers_fields = [
            'codigo_tributacao',
            'atv_economica_normalized',
            'numero_nfs',
            'opt_simples_nacional'
        ]
        data_as_dict = values.model_dump()
        fields_that_doesnt_passed_the_condition = []
        
        for field in only_numbers_fields:
            for char in data_as_dict[field]:
                if not char.isdigit():
                    fields_that_doesnt_passed_the_condition.append(field)
                    break
    
        if fields_that_doesnt_passed_the_condition:
            raise ValueError(f"The following fields must contain only numbers: {fields_that_doesnt_passed_the_condition}")
        
        return values
    
class NotaConvertedInfo(BaseModel):
    
    numero_nfs: int
    codigo_autenticidade: str
    
    data_competencia: date
    
    valor_liquido: float
    valor_total: float 
    valor_deducoes: float 
    valor_pis: float
    valor_cofins: float
    valor_inss: float
    valor_irrf: float
    valor_csll: float
    valor_issqn: float
    base_calculo: float
    aliquota: float
    issqn_a_reter: float
    
    estado: EstadoEnum
    
    codigo_tributacao: str 
    discriminacao_servico: str
    opt_simples_nacional: int
    
    serie: Optional[str] = None    
    nfse_substituida: Optional[str] = None 
    valor_outras_retencoes: Optional[float] = None
    data_emissao: Optional[date] = None
    
    atv_economica: str
    atv_economica_normalized: str
    municipio: MunicipioEnum
    
    
    
    
    
    
    
    
    


    

    
    
    
