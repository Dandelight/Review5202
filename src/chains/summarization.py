from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from ..config.settings import settings
from ..core.prompt_manager import PromptManager


class SummarizationChain:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.llm = ChatAnthropic(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
        )

        self.summary_template = """
        You are tasked with summarizing research papers about LLMs and security.
        Please provide a structured summary with:

        1. Title
        2. Key Points (3-5 bullet points)
        3. Main Contributions
        4. Methodology
        5. Results and Conclusions
        6. Future Work

        Paper content: {text}
        """

    async def _get_prompt(self) -> PromptTemplate:
        chain_prompt = await self.prompt_manager.get_chain_prompt(self.summary_template)
        return PromptTemplate(template=chain_prompt, input_variables=["text"])

    async def summarize(self, text: str):
        prompt = await self._get_prompt()
        chain = load_summarize_chain(llm=self.llm, chain_type="stuff", prompt=prompt)
        return await chain.arun(text)
