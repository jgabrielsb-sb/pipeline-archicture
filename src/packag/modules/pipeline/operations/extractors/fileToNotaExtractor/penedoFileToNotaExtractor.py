from packag.modules.pdf_operations import extract_text_from_pdf

import re

from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor

from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError,
)

from packag.modules.utils.logger import get_logger

from packag.models.business import dtoNota

from packag.models import dtoFile

from typing import Type

from packag.modules.pipeline.utils.messages import (
    ExtractMethodErrorMessage,
)

logger = get_logger('operations')

class PenedoFileToNotaExtractor(FileToNotaExtractor):
    def __init__(self, file: Type[dtoFile.File]):
        self.file = file
        self.file_path = file.file_path
        self.text = None
        
    def extract_data(self):
        try:
            self.text = extract_text_from_pdf(self.file_path)
            return self.text
        except (
            FileNotFoundError,
            PermissionError,
            ValueError
        ) as e:
            message = ExtractMethodErrorMessage(
                method_name='extract_data',
                original_exception=e
            )
            
            logger.error(message.get_message())
            
            raise ExtractMethodError(message) 
            
    def _find(self, pattern):
        if not self.text:
            self.extract_data() # pragma: no cover
        
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def _extract_numero_nfs(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Número da Nota:" in line:
                # Look at the next 1-3 lines after this
                for j in range(i + 1, min(i + 4, len(lines))):
                    match = re.search(r'\d{5,}', lines[j])
                    if match:
                        return match.group(0)
        return None  # if nothing found

    def _extract_codigo_autenticidade(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        return self._find(r'Código de Verificação:\s*([A-Z0-9-]+)')

    def _extract_data_competencia(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Nota Fiscal.*?([A-Z]{3}/\d{4})', self.text, re.DOTALL)
        if match:
            return match.group(1)
        return None

    def _extract_valor_liquido(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor Liquido (R$)" in line:
                values_line = lines[i + 1]
                match = re.match(r'([\d.,]+)', values_line)
                if match:
                    return match.group(1)
        return None

    def _extract_valor_total(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        return self._find(r'VALOR TOTAL DA NOTA = R\$ ([\d.,]+)')

    def _extract_valor_deducoes(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor Liquido (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 2:
                    return matches[1]  # second value
        return None

    def _extract_valor_pis(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "PIS (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 3:
                    return matches[2]  # third value
        return None

    def _extract_valor_cofins(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "COFINS (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 1:
                    return matches[0]  # first value
        return None
    
    def _extract_valor_inss(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 2:
                    return matches[1]  # second value
        return None

    def _extract_valor_irrf(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "IRRF (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 5:
                    return matches[4]  # fifth value
        return None


    def _extract_valor_csll(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "CSLL (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 4:
                    return matches[3]  # fourth value
        return None

    def _extract_valor_issqn(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
        
        lines = self.text.splitlines()
        
        for i, line in enumerate(lines):
            if 'Valor do ISS' in line:
                if i + 1 < len(lines):
                    values_line = lines[i + 1]
                    # split values by spaces or tabs
                    values = [v for v in values_line.split()]
                    if len(values) >= 5:
                        return values[4]  # the 5th element is Valor do ISS (index 4)
                    else:
                        return None # pragma: no cover
        
        return None


    def _extract_base_calculo(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Base de Cálculo (R$)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 3:
                    return matches[2]  # third value
        return None

    def _extract_aliquota(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Alíquota (%)" in line:
                values_line = lines[i + 1]
                matches = re.findall(r'[\d.,]+', values_line)
                if len(matches) >= 4:
                    return matches[3]  # fourth value
        return None


    def _extract_issqn_a_reter(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        if re.search(r'ISS Retido:\s*SIM', self.text, re.IGNORECASE):
            return '1'
        elif re.search(r'ISS Retido:\s*NÃO', self.text, re.IGNORECASE):
            return '0'
        else:
            return None


    def _extract_estado(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        return self._find(r'UF:\s*([A-Z]{2})')

    def _extract_codigo_tributacao(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        return self._find(r'Código CNAE:\s*(\d+)')

    def _extract_discriminacao_servico(self):
        if self.text is None:
            self.extract_data() # pragma: no cover

        match = re.search(r'DISCRIMINAÇÃO DOS SERVIÇOS\s*(.*?)(?=VALOR TOTAL DA NOTA)', self.text, re.DOTALL)
        if match:
            discrim_text = match.group(1).strip()
            return discrim_text
        return None

    
    def _extract_opt_simples_nacional(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        if 'Optante pelo Simples Nacional' in self.text:
            return '1'
        elif 'Não optante pelo Simples Nacional' in self.text:
            return '0'
        else:
            return None

    def _extract_serie(self):
        return None

    def _extract_nfse_substituida(self):
        return None  

    def _extract_valor_outras_retencoes(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        return self._find(r'Outras Retenções\(R\$\)\s*([\d.,]+)')

    def _extract_data_emissao(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
        
        lines = self.text.splitlines()
        
        for i, line in enumerate(lines):
            if 'Data e Hora Emissão' in line:
                if i + 1 < len(lines):
                    data_emissao = lines[i + 2].strip()
                    return data_emissao  # return as string
        return None


    def _extract_atv_economica(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        count = 0
        for line in lines:
            if "Código CNAE:" in line:
                capture = True
                continue
            if capture and line.strip():
                count += 1
                if count == 2:  # <-- we want the second non-empty line
                    match = re.match(r'(\d+)', line.strip())
                    if match:
                        return match.group(1)
        return None

    def _extract_municipio(self):
        if self.text is None:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        for i, line in enumerate(lines):
            if "Município de Incidência do ISS:" in line:
                # Look in next 2 lines for 'CITY - ST'
                for j in range(i + 1, min(i + 3, len(lines))):
                    match = re.search(r'([A-ZÇÃÕÁÉÍÓÚ]+) - [A-Z]{2}', lines[j])
                    if match:
                        return match.group(1).title()  # optional: capitalize nicely
        return None
    




    
    
    
    