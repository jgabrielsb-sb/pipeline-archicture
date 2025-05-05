from ...operation import Operation

from packag.models import dtoFile

from packag.modules.utils.logger import get_logger
from packag.models.business import dtoPrestador

from ...utils.exceptions import ValidationError, OperationError

from abc import ABC, abstractmethod

from pydantic import ValidationError as pydantic_ValidationError

from packag.modules.utils.messages import (
    ValidationErrorMessages,
    OperationErrorMessage
)

logger_operation = get_logger('operation_logger')

class FileToPrestadorExtractor(Operation, ABC):
    """
    Extract data from a file.
    
    This operation expects to receive a dtoFile Object as a input;
    Then, it uses the operation class, which has to be a subclass of Operation, to extract the data from the file.
    The output is a dtoNota.PrestadorExtractedInfo object.
    
    To inherit this class, you have to implement the abstract methods to extract the data from the file.
    """
    def _validate_input(self, input_data: dtoFile):
        if not isinstance(input_data, dtoFile.File):
            raise ValidationError(
                function_name='_validate_input',
                input_name='input_data',
                received_type=type(input_data),
                expected_type=type(dtoFile)
            )
        
        return input_data
    
    @abstractmethod
    def _extract_cpf(self):
        pass
    
    @abstractmethod
    def _extract_cnpj(self):
        pass
    
    @abstractmethod
    def _extract_inscricao_municipal(self):
        pass
    
    @abstractmethod
    def _extract_razao_social(self):
        pass
    
    @abstractmethod
    def _extract_endereco(self):
        pass
    
    @abstractmethod
    def _extract_municipio(self):
        pass
    
    @abstractmethod
    def _extract_uf(self):
        pass
    
    @abstractmethod
    def _extract_cep(self):
        pass
    
    @abstractmethod
    def _extract_numero(self):
        pass    
    
    @abstractmethod
    def _extract_bairro(self):
        pass
    
    @abstractmethod
    def _extract_telefone(self):
        pass
    
    @abstractmethod
    def _extract_email(self):
        pass
    
    def get_extract_methods(self):
        return {
            'cpf': self._extract_cpf,
            'cnpj': self._extract_cnpj,
            'inscricao_municipal': self._extract_inscricao_municipal,
            'razao_social': self._extract_razao_social,
            'endereco': self._extract_endereco,
            'municipio': self._extract_municipio,
            'uf': self._extract_uf,
            'cep': self._extract_cep,
            'numero': self._extract_numero,
            'bairro': self._extract_bairro,
            'telefone': self._extract_telefone,
            'email': self._extract_email,
        }
    
    
    def get_all_extracted_info(self):
        info_dict = {}
        
        for field, method in self.get_extract_methods().items():
            info_dict[field] = method()
        
        return info_dict
    
    def validate_output(self, output_data: dict):
        try:
            return dtoPrestador.PrestadorExtractedInfo(**output_data)
        except pydantic_ValidationError as e:
            
            validation_error = ValidationErrorMessages(
                function_name='validate_output',
                input_name='output_data',
                received_type=type(output_data),
                expected_type=type(dtoPrestador.PrestadorExtractedInfo),
            )
            error_message = validation_error.get_message()
            
            logger_operation.error(error_message)
            raise ValidationError(validation_error)
            
    def run(self, input_data: dtoFile):
        try:
            input_data = self._validate_input(input_data)
            
            output_data = self.get_all_extracted_info()
            
            prestador = self.validate_output(output_data)
            return prestador
        except ValidationError as e:
            message = OperationErrorMessage(
                operation_name='FileToPrestadorExtractor',
                original_exception=e
            )
            logger_operation.error(message.get_message())
            raise OperationError(
                message=message,
                original_exception=e
            ) from e
        except OperationError as e:
            message = OperationErrorMessage(
                operation_name='FileToPrestadorExtractor',
                original_exception=e
            )
            logger_operation.error(message.get_message())
            raise OperationError(
                message=message,
                original_exception=e
            ) from e
        
        

