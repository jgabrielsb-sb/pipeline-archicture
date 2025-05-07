from ....operation import Operation

from packag.models import dtoFile

from packag.modules.utils.logger import get_logger
from packag.models.business import (
    dtoPrestador,
)

from typing import Callable

from ....utils.exceptions import (
    ValidationError, 
    OperationError, 
    ValidationError,
    ExtractMethodError,
    GetAllExtractedInfoError,
)

from abc import ABC, abstractmethod

from pydantic import ValidationError as pydantic_ValidationError

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
    OperationErrorMessage,
    ExtractMethodErrorMessage,
    GetAllExtractedInfoErrorMessage,
)

logger_operation = get_logger('operation_logger')

class FileToPrestadorExtractor(Operation, ABC):
    """
    Extract data from a file.
    
    This operation expects to receive a dtoFile Object as a input;
    Then, it uses the operation class, which has to be a subclass of Operation, to extract the data from the file.
    The output is a dtoPrestador.PrestadorExtractedInfo object.
    
    To inherit this class, you have to implement the abstract methods to extract the data from the file.
    """
    def validate_input(self, input_data: dtoFile):
        """
        Validate the input data.
        If the input data is not a dtoFile object, a ValidationError is raised.
        If the input data is a dtoFile object, it is returned.
        """
        if not isinstance(input_data, dtoFile.File):
            message = ValidationErrorMessage(
                    function_name='validate_input',
                    input_name='input_data',
                    received_type=str(type(input_data)),
                    expected_type=str(type(dtoFile))
                )
            
            logger_operation.error(message.get_message())
            raise ValidationError(message)
        
        return input_data
    
    @abstractmethod
    def _extract_cpf(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_cnpj(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_inscricao_municipal(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_razao_social(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_endereco(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_municipio(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_uf(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_cep(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_numero(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_bairro(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_telefone(self):
        pass # pragma: no cover
    
    @abstractmethod
    def _extract_email(self):
        pass # pragma: no cover
    
    def get_extract_methods(self):
        """
        Get the extract methods.
        The methods are the ones that will be called to extract the data from the file.
        The keys are the names of the fields to be extracted.
        The values are the methods that will be called to extract the data from the file.
        """
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
        
    def run_extract_method(self, method: Callable):
        """
        Run the extract method.
        If the method raises an exception, an ExtractMethodError is raised.
        If the method returns a value, it is returned.
        """
        try:
            return method()
        except Exception as e:
            message = ExtractMethodErrorMessage(
                method_name=method.__name__,
                original_exception=e
                )
            
            logger_operation.error(message.get_message())
            
            raise ExtractMethodError(message)
    
    
    def get_all_extracted_info(self):
        """
        Get all the extracted info.
        The info is a dictionary with the fields as keys and the extracted values as values.
        If an exception is raised, it is appended to the exceptions_raised list.
        If all the methods are executed without raising an exception, the info_dict is returned.
        If an exception is raised, a GetAllExtractedInfoError is raised.
        """
        info_dict = {}
        
        exceptions_raised = []
       
        for field, method in self.get_extract_methods().items():
            try:
                info_dict[field] = self.run_extract_method(method)
            except ExtractMethodError as e:
                exceptions_raised.append(e.message)
                logger_operation.error(e)
                
        if exceptions_raised:
            message = GetAllExtractedInfoErrorMessage(
                exceptions=exceptions_raised
                )
            
            logger_operation.error(message.get_message())
            
            raise GetAllExtractedInfoError(message)
        
        return info_dict
    
    def validate_output(self, output_data: dict):
        """
        Validate the output data.
        If the output data is not a dtoPrestador.PrestadorExtractedInfo object, a ValidationError is raised.
        If the output data is a dtoPrestador.PrestadorExtractedInfo object, it is returned.
        """
        
        if not isinstance(output_data, dict):
            message = ValidationErrorMessage(
                function_name='validate_output',
                input_name='output_data',
                received_type=str(type(output_data)),
                expected_type=str(type(dtoPrestador.PrestadorExtractedInfo)),
            )
            
            logger_operation.error(message.get_message())
            
            raise ValidationError(message)
        
        try:
            return dtoPrestador.PrestadorExtractedInfo(**output_data)
        except pydantic_ValidationError as e:
            message = ValidationErrorMessage(
                function_name='validate_output',
                input_name='output_data',
                received_type=str(type(output_data)),
                expected_type=str(type(dtoPrestador.PrestadorExtractedInfo)),
            )
            error_message = message.get_message()
            
            logger_operation.error(error_message)
            
            raise ValidationError(message)
            
    def run(self, input_data: dtoFile):
        """
        Run the operation.
        The operation is the following:
            * validate the input data;
            * get all the extracted info;
            * validate the output data;
            * return the output data.
        If an exception is raised, an OperationError is raised.
        """
        try:
            input_data = self.validate_input(input_data)
            
            output_data = self.get_all_extracted_info()
            
            nota = self.validate_output(output_data)
            return nota
        except (
            ValidationError, 
            GetAllExtractedInfoError
        ) as e:
            message = OperationErrorMessage(
                operation_name='run',
                original_exception=e
                )
            
            logger_operation.error(message.get_message())
            
            raise OperationError(message)
        
        

