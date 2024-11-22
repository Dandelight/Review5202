from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseExtractor(ABC):
    @abstractmethod
    async def extract_text(self, pdf_path: Path) -> Optional[str]:
        pass

    @abstractmethod
    async def save_markdown(self, content: str, output_path: Path) -> bool:
        pass
