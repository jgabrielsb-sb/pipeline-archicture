from pydantic import (
    BaseModel,
    ConfigDict
)
from typing import Optional

import datetime

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
    
    
    
    
    


    

    
    
    
