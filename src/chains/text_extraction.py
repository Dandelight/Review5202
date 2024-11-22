from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..extractors.nougat import NougatExtractor
from ..extractors.pypdf import PyPDFExtractor

# Reference existing PDFExtractor implementation
# startLine: 13
# endLine: 144
