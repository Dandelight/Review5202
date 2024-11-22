from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from ..config.settings import settings
from ..core.prompt_manager import PromptManager
from ..core.scholarly_client import ScholarlyClient


class PaperCollectionChain:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.scholarly_client = ScholarlyClient()
        self.llm = ChatAnthropic(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
        )

        self.search_template = """
        You are tasked with finding relevant academic papers.
        Please analyze the following topic and suggest specific search terms
        that will yield recent and technically detailed papers:

        Topic: {topic}

        Focus on papers that:
        1. Contain novel technical contributions
        2. Are recent (preferably within the last 2 years)
        3. Have significant citations or are from reputable sources
        """

    async def _get_prompt(self) -> PromptTemplate:
        chain_prompt = await self.prompt_manager.get_chain_prompt(self.search_template)
        return PromptTemplate(template=chain_prompt, input_variables=["topic"])

    async def run(self, topic: str):
        prompt = await self._get_prompt()
        chain = LLMChain(llm=self.llm, prompt=prompt)
        search_query = await chain.arun(topic=topic)
        papers = await self.scholarly_client.search_papers(search_query)
        return papers
