from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from ..config.settings import settings


class SummarizationChain:
    def __init__(self):
        self.llm = ChatAnthropic(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
        )

        self.summary_template = """
        Summarize this research paper with the following structure:
        1. Title
        2. Key Points (3-5 bullet points)
        3. Main Contributions
        4. Methodology
        5. Results and Conclusions
        6. Future Work

        Paper content: {text}
        """

        self.prompt = PromptTemplate(
            template=self.summary_template, input_variables=["text"]
        )

        self.chain = load_summarize_chain(
            llm=self.llm, chain_type="stuff", prompt=self.prompt
        )

    async def summarize(self, text: str):
        return await self.chain.arun(text)
