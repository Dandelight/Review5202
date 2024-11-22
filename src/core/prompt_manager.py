from pathlib import Path
from typing import Optional

import aiofiles

from ..config.settings import settings


class PromptManager:
    def __init__(self):
        self.base_prompt_path = Path(
            "Thinking-Claude/model_instructions/v4-20241118.md"
        )
        self._system_prompt: Optional[str] = None

    async def load_system_prompt(self) -> str:
        """Load and cache the system prompt from file."""
        if self._system_prompt is None:
            try:
                async with aiofiles.open(
                    self.base_prompt_path, "r", encoding="utf-8"
                ) as f:
                    self._system_prompt = await f.read()
            except Exception as e:
                print(f"Error loading system prompt: {e}")
                self._system_prompt = ""
        return self._system_prompt

    async def get_chain_prompt(self, chain_specific_prompt: str) -> str:
        """Combine system prompt with chain-specific instructions."""
        system_prompt = await self.load_system_prompt()
        return f"{system_prompt}\n\nAdditional Instructions:\n{chain_specific_prompt}"
