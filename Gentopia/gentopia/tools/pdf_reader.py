import io
import requests
from PyPDF2 import PdfReader
from typing import Optional, Type, Any, List
from pydantic import BaseModel, Field
from gentopia.tools.basetool import BaseTool

class ReadPDFOnlineArgs(BaseModel):
    url: str = Field(..., description="URL of the PDF to read")

class PDFReaderTool(BaseTool):
    """Tool to read content from an online PDF file."""

    name = "pdf_reader"
    description = "A tool to read and extract text from an online PDF file."
    args_schema: Optional[Type[BaseModel]] = ReadPDFOnlineArgs

    def split_text_into_chunks(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Split text into chunks with a maximum size of `max_chunk_size`."""
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        return chunks

    def process_chunks(self, chunks: List[str]) -> None:
        """Process each text chunk. Placeholder for actual processing logic."""
        # Example: Print the first 100 characters of each chunk to demonstrate
        for chunk in chunks:
            print(chunk[:100], "...\n")

    def _run(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()

        with io.BytesIO(response.content) as f:
            reader = PdfReader(f)
            text = []
            for page in reader.pages:
                page_text = page.extract_text() if page.extract_text() else ""
                text.append(page_text)
            full_text = '\n\n'.join(text)

        # Split the extracted text into chunks
        chunks = self.split_text_into_chunks(full_text, max_chunk_size=1000)

        # Process each chunk
        self.process_chunks(chunks)

        return "Completed processing PDF."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example usage
    url = "https://arxiv.org/pdf/2106.14812.pdf"  # Example PDF URL
    PDFReaderTool()._run(url)
