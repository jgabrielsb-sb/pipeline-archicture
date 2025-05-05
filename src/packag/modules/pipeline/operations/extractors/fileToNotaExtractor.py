from ...operation import Operation

from packag.models import dtoFile

from packag.modules.utils.logger import get_logger
from packag.models.business import dtoNota

from ...utils.exceptions import ValidationError, OperationError

from abc import ABC, abstractmethod

from pydantic import ValidationError as pydantic_ValidationError

from packag.modules.utils.messages import ValidationErrorMessages

logger_operation = get_logger('operation_logger')

class FileToNotaExtractor(Operation, ABC):
    """
    Extract data from a file.
    
    This operation expects to receive a dtoFile Object as a input;
    Then, it uses the operation class, which has to be a subclass of Operation, to extract the data from the file.
    The output is a dtoNota.NotaExtractedInfo object.
    
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
    def _extract_numero_nfs(self):
        pass
    
    @abstractmethod
    def _extract_codigo_autenticidade(self):
        pass
    
    @abstractmethod
    def _extract_data_competencia(self):
        pass
    
    @abstractmethod
    def _extract_valor_liquido(self):
        pass
    
    @abstractmethod
    def _extract_valor_total(self):
        pass
    
    @abstractmethod
    def _extract_valor_deducoes(self):
        pass
    
    @abstractmethod
    def _extract_valor_pis(self):
        pass
    
    @abstractmethod
    def _extract_valor_cofins(self):
        pass
    
    @abstractmethod
    def _extract_valor_inss(self):
        pass
    
    @abstractmethod
    def _extract_valor_irrf(self):
        pass
    
    @abstractmethod
    def _extract_valor_csll(self):
        pass
    
    @abstractmethod
    def _extract_valor_issqn(self):
        pass
    
    @abstractmethod
    def _extract_base_calculo(self):
        pass
    
    @abstractmethod
    def _extract_aliquota(self):
        pass
    
    @abstractmethod
    def _extract_issqn_a_reter(self):
        pass
    
    @abstractmethod
    def _extract_issqn_a_reter(self):
        pass
    
    @abstractmethod
    def _extract_estado(self):
        pass
    
    @abstractmethod
    def _extract_codigo_tributacao(self):
        pass
    
    @abstractmethod
    def _extract_discriminacao_servico(self):
        pass
    
    @abstractmethod
    def _extract_opt_simples_nacional(self):
        pass
    
    @abstractmethod
    def _extract_serie(self):
        pass
    
    @abstractmethod
    def _extract_nfse_substituida(self):
        pass
    
    @abstractmethod
    def _extract_valor_outras_retencoes(self):
        pass
    
    @abstractmethod
    def _extract_data_emissao(self):
        pass
    
    @abstractmethod
    def _extract_atv_economica(self):
        pass
    
    @abstractmethod
    def _extract_municipio(self):
        pass
    
    def get_extract_methods(self):
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
    
    
    def get_all_extracted_info(self):
        info_dict = {}
        
        for field, method in self.get_extract_methods().items():
            info_dict[field] = method()
        
        return info_dict
    
    def validate_output(self, output_data: dict):
        try:
            return dtoNota.NotaExtractedInfo(**output_data)
        except pydantic_ValidationError as e:
            
            validation_error = ValidationErrorMessages(
                function_name='validate_output',
                input_name='output_data',
                received_type=type(output_data),
                expected_type=type(dtoNota.NotaExtractedInfo),
            )
            error_message = validation_error.get_message()
            
            logger_operation.error(error_message)
            raise ValidationError(validation_error)
            
    def run(self, input_data: dtoFile):
        try:
            input_data = self._validate_input(input_data)
            
            output_data = self.get_all_extracted_info()
            
            nota = self.validate_output(output_data)
            return nota
        except ValidationError as e:
            raise OperationError(e)
        except OperationError as e:
            raise OperationError(e)
        
        
if __name__ == '__main__':
        pass
        

