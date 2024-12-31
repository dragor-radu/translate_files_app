import os
from PyPDF2 import PdfReader
import docx

class DocParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extracted_text = self._extract_text()

    def _extract_text(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")
        
        _, file_extension = os.path.splitext(self.file_path)
        file_extension = file_extension.lower()

        if file_extension == '.pdf':
            return self._extract_text_from_pdf()
        elif file_extension == '.txt':
            return self._extract_text_from_txt()
        elif file_extension == '.docx':
            return self._extract_text_from_docx()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

    def _extract_text_from_pdf(self):
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")
        return text

    def _extract_text_from_txt(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Failed to extract text from TXT file: {e}")

    def _extract_text_from_docx(self):
        try:
            doc = docx.Document(self.file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX file: {e}")

