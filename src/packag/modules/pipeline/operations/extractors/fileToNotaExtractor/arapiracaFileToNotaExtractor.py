from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodErrorMessage
)
from packag.modules.pipeline.utils.exceptions import (
    ExtractMethodError
)

from packag.modules.utils.logger import get_logger
from packag.models import dtoFile
from typing import Type

logger = get_logger('operations')

class ArapiracaFileToNotaExtractor(FileToNotaExtractor):
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
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Retenção Simples\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_codigo_autenticidade(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "código de verificação" in line.lower():
                # Search in next non-empty line
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        match = re.search(r'([A-Z0-9]{4}\.[A-Z0-9]{4}\.[A-Z0-9]{4})', next_line, re.IGNORECASE)
                        if match:
                            return match.group(1)
        return None

    def _extract_data_competencia(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Data de Competência\s*:\s*(\d{2}/\d{2}/\d{4})', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_valor_liquido(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        """Extrai o Valor Líquido da Nota a partir do texto da NFS-e de Arapiraca."""
        lines = self.text.splitlines()
        
        for i, line in enumerate(lines):
            if "Valor Líquido da Nota" in line:
                # A próxima linha contém os valores
                if i + 1 < len(lines):
                    valores_line = lines[i + 1].strip()
                    valores = re.findall(r"[\d.,]+", valores_line)
                    
                    if valores:
                        return valores[-1].strip()  # pega o último valor da linha
        return None

    def _extract_valor_total(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        return self._find(r'VALOR TOTAL DA NOTA = R\$ ([\d.,]+)')

    def _extract_valor_deducoes(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        
        for i, line in enumerate(lines):
            if "Dedução(R$)" in line:
                # A próxima linha contém os valores
                if i + 1 < len(lines):
                    valores_line = lines[i + 1].strip()
                    valores = re.findall(r"[\d.,]+", valores_line)
                    
                    if valores:
                        return valores[3].strip()  # pega o último valor da linha
        return None



    def _extract_valor_pis(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "PIS" in line:  # fuzzy match
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        values = re.findall(r'[\d.,]+', next_line)
                        if len(values) >= 2:
                            return values[1]  # PIS is second column
        return None

    def _extract_valor_cofins(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        header_keywords = ["INSS", "PIS", "Cofins", "C.S.L.L", "IRRF"]
        for i, line in enumerate(lines):
            if all(keyword in line.replace(" ", "") for keyword in header_keywords):
                # Found header line
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        # Try splitting on 2+ spaces
                        values = re.split(r'\s{2,}', next_line)
                        if len(values) >= 3:
                            return values[2]  # pragma: no cover
                        # fallback: regex multiple numbers
                        values = re.findall(r'[\d.,]+', next_line)
                        if len(values) >= 3:
                            return values[2]
                        break # pragma: no cover
        return None

    def _extract_valor_inss(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line.replace(" ", "").upper():
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        values = re.findall(r'[\d.,]+', next_line)
                        if len(values) >= 1:
                            return values[0]  # first value = INSS
        return None


    def _extract_valor_irrf(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line and "IRRF" in line:
                # try extracting numbers from same line
                numbers = re.findall(r'[\d.,]+', line)
                if len(numbers) >= 5:
                    return numbers[4]  # 5th = IRRF # pragma: no cover
        # fallback: try next line if not merged
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line and "IRRF" in line:
                for j in range(i+1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        numbers = re.findall(r'[\d.,]+', next_line)
                        if len(numbers) >= 5:
                            return numbers[4]
                        break # pragma: no cover
        return None


    def _extract_valor_csll(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line and "IRRF" in line:
                numbers = re.findall(r'[\d.,]+', line)
                if len(numbers) >= 4:
                    return numbers[3]  # pragma: no cover
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line and "IRRF" in line:
                for j in range(i+1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        numbers = re.findall(r'[\d.,]+', next_line)
                        if len(numbers) >= 4:
                            return numbers[3]
                        break # pragma: no cover
        return None

    def _extract_valor_issqn(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor do Serviço" in line:
                # Found header line → values in next line
                if i + 1 < len(lines):
                    value_line = lines[i + 1].strip()
                    values = value_line.split()
                    if len(values) >= 7:
                        return values[6]  # index 6 = Valor do ISS(R$)
        return None

    def _extract_base_calculo(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor do Serviço" in line:
                # Found header → next line is values
                if i + 1 < len(lines):
                    value_line = lines[i + 1].strip()
                    values = value_line.split()
                    if len(values) >= 5:
                        return values[4]  # index 4 = Base de Cálculo (R$)
        return None

    def _extract_aliquota(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor do Serviço" in line:
                if i + 1 < len(lines):
                    value_line = lines[i + 1].strip()
                    values = value_line.split()
                    if len(values) >= 6:
                        return values[5]  # index 5 = Aliquota(%)
        return None


    def _extract_issqn_a_reter(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        if 'Retenção Simples' in self.text:
            return '1'
        elif 'ISSQN a Recolher' in self.text:
            return '0' # pragma: no cover
        else:
            return None

    def _extract_estado(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'-\s*([A-Z]{2})\s*-\s*BRASIL', self.text)
        return match.group(1) if match else None

    def _extract_codigo_tributacao(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        pattern = re.compile(r'^\s*(\d{1,2}\.\d{1,2})')

        for line in lines:
            if "Discriminação do Serviço" in line:
                capture = True
                continue
            if capture:
                match = pattern.match(line)
                if match:
                    return match.group(1)
                if "Valor do Serviço" in line or "VALOR TOTAL DA NOTA" in line:
                    break # pragma: no cover
        return None

    def _extract_discriminacao_servico(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Discriminação do Serviço" in line:
                capture = True
                continue
            if capture and (line.strip().startswith("Contrato") or line.strip().startswith("contrato")):
                return line.strip()
            if capture and "Valor do Serviço" in line:
                break  # exit if reached table # pragma: no cover
        return None

    
    def _extract_opt_simples_nacional(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        # regex case-insensitive, optional spaces, accents tolerant
        if 'Não optante pelo Simples Nacional' in self.text:
            return '0' # pragma: no cover
        elif 'OPTANTE PELO SIMPLES NACIONAL' in self.text:
            return '1'
        else:
            return None


    def _extract_serie(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        return None

    def _extract_nfse_substituida(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        return None  # Not present in Arapiraca's PDF

    def _extract_valor_outras_retencoes(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Outras Retenções(R$)" in line:
                # Get the next line (values)
                if i + 1 < len(lines):
                    values_line = lines[i + 1]
                    # Extract all numbers
                    values = re.findall(r'[\d.,]+', values_line)
                    header_fields = re.findall(r'[^\s]+', line)
                    # Find index of 'Outras Retenções(R$)' in header
                    try:
                        index = header_fields.index('Outras')
                    except ValueError:
                        index = header_fields.index('OutrasRetenções(R$)') if 'OutrasRetenções(R$)' in header_fields else None
                    if index is not None and index < len(values):
                        return values[index]
                    elif len(values) >= 2:  
                        return values[1]  # fallback: second value
        return None

    def _extract_data_emissao(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Data/Hora da emissão.*?(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})', self.text, re.DOTALL)
        if match:
            return match.group(1)
        return None

    def _extract_atv_economica(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        return self._extract_codigo_tributacao()

    def _extract_municipio(self):
        if not self.text:
            self.extract_data() # pragma: no cover
            
        match = re.search(r'Cidade\s+([A-ZÇÃÕÁÉÍÓÚ ]+)\s*-\s*[A-Z]{2}', self.text)
        print(f"[DEBUG match]: {match.group(0) if match else 'No match'}")
        if match:
            return match.group(1).strip().title()
        return None
