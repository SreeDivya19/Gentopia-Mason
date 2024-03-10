from transformers import pipeline
from typing import Any, Optional, Type
from pydantic import BaseModel, Field

from gentopia.tools.basetool import BaseTool


class SummarizeTextArgs(BaseModel):
    text: str = Field(..., description="Text to summarize")


class TextSummarizerTool(BaseTool):
    """summarize text using a pre-trained model."""

    name = "text_summarizer"
    description = "A tool to automatically summarize text."
    args_schema: Optional[Type[BaseModel]] = SummarizeTextArgs

    def _run(self, text: str) -> str:
        # Load the summarization pipeline
        summarizer = pipeline("summarization")
        # Generate summary
        summary_list = summarizer(text, max_length=130, min_length=30, do_sample=False)
        summary_text = " ".join([summary['summary_text'] for summary in summary_list])
        return summary_text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    text = "extracted text"
    summarizer = TextSummarizerTool()
    summary = summarizer._run(text)
    print(summary)
