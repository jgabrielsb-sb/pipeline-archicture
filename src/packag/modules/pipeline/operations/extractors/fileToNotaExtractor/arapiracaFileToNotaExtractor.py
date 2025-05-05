from packag.modules.pdf_operations import extract_text_from_pdf
from pathlib import Path
import re
from packag.modules.pipeline.operations.extractors.fileToNotaExtractor import FileToNotaExtractor
from packag.modules.pipeline.utils.exceptions import OperationError
from packag.modules.utils.logger import get_logger
from packag.models.dtoFile import File
from typing import Type


logger = get_logger('operations')

class ArapiracaFileToNotaExtractor(FileToNotaExtractor):
    def __init__(self, file: Type[File]):
        self.file = file
        self.file_path = file.file_path
        self.text = self.extract_data()

    def extract_data(self):
        try:
            self.text = extract_text_from_pdf(self.file_path)
            return self.text
        
        except FileNotFoundError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"File {self.file_path} not found",
                original_exception=e
            ) from e
            
        except ValueError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"Error extracting data from file: {e}",
                original_exception=e
            ) from e
            
        except PermissionError as e:
            logger.error(f"Error extracting data from file: {e}")
            raise OperationError(
                message=f"Error extracting data from file: {e}",
                original_exception=e
            ) from e

    def _find(self, pattern):
        if not self.text:
            self.extract_data()
        
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def _extract_numero_nfs(self):
        match = re.search(r'Retenção Simples\s*(\d+)', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_codigo_autenticidade(self):
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
        match = re.search(r'Data de Competência\s*:\s*(\d{2}/\d{2}/\d{4})', self.text)
        if match:
            return match.group(1)
        return None

    def _extract_valor_liquido(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Valor Líquido da Nota" in line:  # match substring (ignore accents if OCR removed)
                # Get next non-empty line
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        match = re.match(r'([\d.,]+)', next_line)
                        if match:
                            return match.group(1)
        return None

    def _extract_valor_total(self):
        return self._find(r'VALOR TOTAL DA NOTA = R\$ ([\d.,]+)')

    def _extract_valor_deducoes(self):
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "Dedução(R$)" in line:
                # Get next non-empty line
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        values = re.findall(r'[\d.,]+', next_line)
                        index = line.split().index("Dedução(R$)")
                        if index < len(values):
                            return values[index]
                        break
        return None


    def _extract_valor_pis(self):
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
                            return values[2]  # third column = Cofins
                        # fallback: regex multiple numbers
                        values = re.findall(r'[\d.,]+', next_line)
                        if len(values) >= 3:
                            return values[2]
                        break
        return None

    def _extract_valor_inss(self):
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
        for line in self.text.splitlines():
            if "INSS" in line and "IRRF" in line:
                # try extracting numbers from same line
                numbers = re.findall(r'[\d.,]+', line)
                if len(numbers) >= 5:
                    return numbers[4]  # 5th = IRRF
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
                        break
        return None


    def _extract_valor_csll(self):
        for line in self.text.splitlines():
            if "INSS" in line and "IRRF" in line:
                numbers = re.findall(r'[\d.,]+', line)
                if len(numbers) >= 4:
                    return numbers[3]  # 4th = C.S.L.L
        lines = self.text.splitlines()
        for i, line in enumerate(lines):
            if "INSS" in line and "IRRF" in line:
                for j in range(i+1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line:
                        numbers = re.findall(r'[\d.,]+', next_line)
                        if len(numbers) >= 4:
                            return numbers[3]
                        break
        return None

    def _extract_valor_issqn(self):
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
        return '1' if 'ISS Retido:\s*SIM' in self.text else '0'

    def _extract_estado(self):
        match = re.search(r'-\s*([A-Z]{2})\s*-\s*BRASIL', self.text)
        return match.group(1) if match else None

    def _extract_codigo_tributacao(self):
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Discriminação do Serviço" in line:
                capture = True
                continue
            if capture:
                # Look for line starting with number pattern
                match = re.match(r'\s*(\d{2}\.\d{2})', line)
                if match:
                    return match.group(1)
                # stop search if passed that block
                if "Valor do Serviço" in line or "VALOR TOTAL DA NOTA" in line:
                    break
        return None

    def _extract_discriminacao_servico(self):
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Discriminação do Serviço" in line:
                capture = True
                continue
            if capture and line.strip().startswith("Contrato"):
                return line.strip()
            if capture and "Valor do Serviço" in line:
                break  # exit if reached table
        return None

    
    def _extract_opt_simples_nacional(self):
        # regex case-insensitive, optional spaces, accents tolerant
        match = re.search(r'optante\s+.*simples\s+nacional', self.text, re.IGNORECASE)
        return '1' if match else '0'


    def _extract_serie(self):
        return None

    def _extract_nfse_substituida(self):
        return None  # Not present in Arapiraca's PDF

    def _extract_valor_outras_retencoes(self):
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
        match = re.search(r'Data/Hora da emissão.*?(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})', self.text, re.DOTALL)
        if match:
            return match.group(1)
        return None

    def _extract_atv_economica(self):
        lines = self.text.splitlines()
        capture = False
        for line in lines:
            if "Discriminação do Serviço" in line:
                capture = True
                continue
            if capture:
                # Look for line starting with number pattern
                match = re.match(r'\s*(\d{2}\.\d{2})', line)
                if match:
                    return match.group(1)
                # stop search if passed that block
                if "Valor do Serviço" in line or "VALOR TOTAL DA NOTA" in line:
                    break
        return None

    def _extract_municipio(self):
        match = re.search(r'Cidade\s+([A-ZÇÃÕÁÉÍÓÚ ]+)\s*-\s*[A-Z]{2}', self.text)
        print(f"[DEBUG match]: {match.group(0) if match else 'No match'}")
        if match:
            return match.group(1).strip().title()
        return None



if __name__ == "__main__":
    dtoFile =  File(
        file_path=Path('static/notas_fiscais/arapiraca/205.pdf'),
        file_extension='pdf'
    )
    arapiraca_file_to_nota_extractor = ArapiracaFileToNotaExtractor(dtoFile)
    print(arapiraca_file_to_nota_extractor.run(dtoFile))
    
    