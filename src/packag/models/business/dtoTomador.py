from pydantic import BaseModel, model_validator
from typing import Optional
from packag.models.business.enum import (
    EstadoEnum,
    MunicipioEnum
)

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
    
class TomadorFormattedInfo(BaseModel):
    cnpj: Optional[str] = None
    cpf: Optional[str] = None
    inscricao_municipal: str
    razao_social: str
    
    endereco: str
    municipio: MunicipioEnum
    uf: EstadoEnum
    cep: str
    
    numero: Optional[int] = None
    bairro: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    
    
    @model_validator(mode='after')   # must have at least one of the following fields: cnpj or cpf
    def at_least_one_document(cls, values):
        if not values.cnpj and not values.cpf:
            raise ValueError('At least one of cnpj or cpf must be provided.')
        return values
    
    @model_validator(mode='after')   # must have only numbers in the following fields: cnpj, cpf, inscricao_municipal, cep, telefone
    def only_numbers(cls, values):
        only_numbers_fields = [
            'cnpj',
            'cpf',
            'inscricao_municipal',
            'cep',
            'telefone'
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
