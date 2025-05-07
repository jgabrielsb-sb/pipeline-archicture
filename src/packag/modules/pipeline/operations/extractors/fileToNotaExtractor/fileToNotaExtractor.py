from ....operation import Operation

from packag.models import dtoFile

from packag.modules.utils.logger import get_logger
from packag.models.business import dtoNota

from ....utils.exceptions import (
    ValidationError, 
    OperationError,
    ExtractMethodError,
    GetAllExtractedInfoError
)

from typing import Callable

from abc import ABC, abstractmethod

from pydantic import ValidationError as pydantic_ValidationError

from packag.modules.pipeline.utils.messages import (
    ValidationErrorMessage,
    ExtractMethodErrorMessage,
    OperationErrorMessage,
    GetAllExtractedInfoErrorMessage
)

logger_operation = get_logger('operation_logger')

class FileToNotaExtractor(Operation, ABC):
    """
    Abstract base class for extracting structured invoice data (Nota) from a file.

    This class defines the structure (blueprint) for creating extraction operations that convert
    a raw `dtoFile` object (representing a file input) into a validated `dtoNota.NotaExtractedInfo`
    object, ensuring robust error handling, logging, and field-level extraction.

    👉 Intended usage:
        The **only method intended to be called directly by the end user is `run(input_data)`**.
        The `run()` method orchestrates the entire extraction process:
            - validates the input
            - runs all field extraction methods
            - validates the extracted output
            - logs all steps and errors
            - catches and wraps any raised exceptions
        If an error occurs at any step, it is logged and **raised as an `OperationError`** to 
        signal a failure in the extraction process in a unified way.

    Core Workflow of `run(input_data)`:
        1. Validate input object type.
        2. Sequentially execute each extraction method (one per field).
        3. Collect extracted field values into a dictionary.
        4. Validate the extracted data against the `NotaExtractedInfo` model.
        5. Return a validated Nota object.

    Subclass Requirements:
        - Subclasses must implement **all abstract `_extract_<field>()` methods** to define 
          how each specific field is extracted from the input file.
        - Subclasses should not override `run()`, `get_all_extracted_info()`, or `validate_input()` 
          unless extending or altering core behavior intentionally.

    Example Usage:
        class MyExtractor(FileToNotaExtractor):
            def _extract_numero_nfs(self): ...
            def _extract_codigo_autenticidade(self): ...
            ... (implement all other abstract methods) ...

        extractor = MyExtractor()
        nota = extractor.run(input_file)

    Attributes:
        logger_operation: Logger object used for recording extraction, validation, and error events.

    Raises:
        ValidationError: If input data or output validation fails (wrapped into OperationError by `run`).
        ExtractMethodError: If one or more field extraction methods fail (wrapped into OperationError by `run`).
        OperationError: Raised by `run()` if any step in the process fails, encapsulating the original error.
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
    def _extract_numero_nfs(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_codigo_autenticidade(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_data_competencia(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_liquido(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_total(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_deducoes(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_pis(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_cofins(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_inss(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_irrf(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_csll(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_issqn(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_base_calculo(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_aliquota(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_issqn_a_reter(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_issqn_a_reter(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_estado(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_codigo_tributacao(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_discriminacao_servico(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_opt_simples_nacional(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_serie(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_nfse_substituida(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_valor_outras_retencoes(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_data_emissao(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_atv_economica(self): # pragma: no cover
        pass
    
    @abstractmethod
    def _extract_municipio(self): # pragma: no cover
        pass
    
    def get_extract_methods(self):
        """
        Get the extract methods.
        The methods are the ones that will be called to extract the data from the file.
        The keys are the names of the fields to be extracted.
        The values are the methods that will be called to extract the data from the file.
        """
        return {
            'numero_nfs': self._extract_numero_nfs,
            'codigo_autenticidade': self._extract_codigo_autenticidade,
            'data_competencia': self._extract_data_competencia,
            'valor_liquido': self._extract_valor_liquido,
            'valor_total': self._extract_valor_total,
            'valor_deducoes': self._extract_valor_deducoes,
            'valor_pis': self._extract_valor_pis,
            'valor_cofins': self._extract_valor_cofins,
            'valor_inss': self._extract_valor_inss,
            'valor_irrf': self._extract_valor_irrf,
            'valor_csll': self._extract_valor_csll,
            'valor_issqn': self._extract_valor_issqn,
            'base_calculo': self._extract_base_calculo,
            'aliquota': self._extract_aliquota,
            'issqn_a_reter': self._extract_issqn_a_reter,
            'estado': self._extract_estado,
            'codigo_tributacao': self._extract_codigo_tributacao,
            'discriminacao_servico': self._extract_discriminacao_servico,
            'opt_simples_nacional': self._extract_opt_simples_nacional,
            'serie': self._extract_serie,
            'nfse_substituida': self._extract_nfse_substituida,
            'valor_outras_retencoes': self._extract_valor_outras_retencoes,
            'data_emissao': self._extract_data_emissao,
            'atv_economica': self._extract_atv_economica,
            'municipio': self._extract_municipio,
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
        If the output data is not a dtoNota.NotaExtractedInfo object, a ValidationError is raised.
        If the output data is a dtoNota.NotaExtractedInfo object, it is returned.
        """
        
        if not isinstance(output_data, dict):
            message = ValidationErrorMessage(
                function_name='validate_output',
                input_name='output_data',
                received_type=str(type(output_data)),
                expected_type=str(type(dtoNota.NotaExtractedInfo)),
            )
            
            logger_operation.error(message.get_message())
            
            raise ValidationError(message)
        
        try:
            return dtoNota.NotaExtractedInfo(**output_data)
        except pydantic_ValidationError as e:
            message = ValidationErrorMessage(
                function_name='validate_output',
                input_name='output_data',
                received_type=str(type(output_data)),
                expected_type=str(type(dtoNota.NotaExtractedInfo)),
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
        
        

        

