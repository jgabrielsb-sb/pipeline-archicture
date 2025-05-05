from pydantic import BaseModel, model_validator
from typing import Optional

class TomadorExtractedInfo(BaseModel):
    cnpj: Optional[str] = None
    cpf: Optional[str] = None
    inscricao_municipal: str
    razao_social: str
    
    endereco: str
    municipio: str
    uf: str
    cep: str
    
    numero: Optional[str] = None
    bairro: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    
    @model_validator(mode='after')
    def at_least_one_document(cls, values):
        if not values.cnpj and not values.cpf:
            raise ValueError('At least one of cnpj or cpf must be provided.')
        return values

class TomadorBase(BaseModel):
    """
    Fields that are required to create a Tomador.
    Those are the common fields that are present in all the other models.
    """
    cnpj: str # cnpj
    razao_social: str # razao_social
    cep: str
    municipio: str
    endereco: str
    
    estado: Optional[str] = None
    numero: Optional[str] = None 
    bairro: Optional[str] = None 
    telefone: Optional[str] = None
    email: Optional[str] = None 
    
class TomadorAfterExtractor(TomadorBase):
    """
    Fields that are extracted from the NFS-e.
    """
    pass

class TomadorAfterEnderecoNormalization(TomadorAfterExtractor):
    """
    Fields that are extracted from the NFS-e.
    Initially, there are some NFS-e that have all the adress fields on the endereco field.
    Then, we must separate the adress into fields like numero, bairro, municipio, estado and cep.
    
    """
    estado: str
    numero: str
    bairro: str
    
    
class TomadorAfterFormatter(TomadorAfterEnderecoNormalization):
    numero: int 

class TomadorDatabase(TomadorAfterFormatter):
    pass