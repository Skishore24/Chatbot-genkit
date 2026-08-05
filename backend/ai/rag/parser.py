from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader


class DocumentParser:

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = []

        reader = PdfReader(file_path)

        for page in reader.pages:
            content = page.extract_text()

            if content:
                text.append(content)

        return "\n".join(text)

    @staticmethod
    def parse_docx(file_path: str) -> str:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    @staticmethod
    def parse_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def parse_website(url: str) -> str:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "GenKit-AI-Chatbot"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            ["script", "style", "noscript"]
        ):
            tag.decompose()

        text = soup.get_text(separator="\n")

        cleaned = []

        for line in text.splitlines():
            line = line.strip()

            if line:
                cleaned.append(line)

        return "\n".join(cleaned)

    @staticmethod
    def parse(file_path: str, website: Optional[bool] = False) -> str:

        if website:
            return DocumentParser.parse_website(file_path)

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return DocumentParser.parse_pdf(file_path)

        if extension == ".docx":
            return DocumentParser.parse_docx(file_path)

        if extension == ".txt":
            return DocumentParser.parse_txt(file_path)

        raise ValueError(
            f"Unsupported file format: {extension}"
        )