from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic

from ..config.settings import settings
from ..core.scholarly_client import ScholarlyClient


class PaperCollectionChain:
    def __init__(self):
        self.scholarly_client = ScholarlyClient()
        self.llm = ChatAnthropic(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
        )

        self.search_prompt = PromptTemplate(
            input_variables=["topic"],
            template="Find recent and relevant papers about {topic} with a focus on technical details and novel contributions.",
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.search_prompt)

    async def run(self, topic: str):
        search_query = await self.chain.arun(topic=topic)
        papers = await self.scholarly_client.search_papers(search_query)
        return papers
