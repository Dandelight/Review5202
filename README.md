# Review 5202

> Still searching link-by-link and reading line-by-line to compose a review in 5202?

A comprehensive Python-based pipeline for collecting, downloading, and analyzing academic papers, with a focus on LLM and Security research papers.

## 🌟 Features

- **Paper Collection**: Scrapes Google Scholar for relevant papers
- **Automated Downloads**: Downloads papers from various academic sources
- **Text Extraction**: Supports multiple PDF extraction methods
- **AI-Powered Summaries**: Generates research paper summaries using Claude 3

## 🛠️ Pipeline Components

### 1. Paper Collection (`generate_papers.py`)

- Scrapes Google Scholar using `scholarly`
- Streams results to markdown in real-time
- Async implementation for better performance
- Outputs structured paper metadata

### 2. Paper Download (`download_papers.py`)

- Async download of papers from URLs
- Smart rate limiting
- Progress tracking
- Filename sanitization
- Handles various academic sources

### 3. Text Extraction (`extract_markdown.py`)

- Dual extraction methods:
  - PyPDF2 (fast, basic extraction)
  - Nougat (ML-based, better accuracy)
- Comparison reporting
- Error handling and validation

### 4. AI Summarization (`summarize_papers.py`)

- Uses Claude 3 API for intelligent summarization
- Structured summary format
- Index generation
- Async processing

## 📋 Requirements

```shell
pip install -r requirements.txt
```

Required packages:

- `scholarly`
- `aiohttp`
- `aiofiles`
- `PyPDF2`
- `nougat-ocr`
- `anthropic-sdk`
- `tqdm`

## 🔑 API Keys

Required API keys:

- Anthropic API key for Claude (for summarization)

Set up your API key:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or I recommend you create a `.env` file and write the keys in it like:

```shell
ANTHROPIC_API_KEY=sk-this-is-your-api-key
# base_url defaults to the official API
# ANTHROPIC_BASE_URL=https://example.com
```

and run it using [`dotenvx`](https://github.com/dotenvx/dotenvx):

```shell
dotenvx run -- python summarize_papers.py
```

## 🚀 Usage

### 1. Collect Papers

```bash
python generate_papers.py
```

Outputs: `papers.md`

### 2. Download Papers

```bash
python download_papers.py
```

Outputs: `papers/*.pdf`

### 3. Extract Text

```bash
python extract_markdown.py
```

Outputs:

- `markdown/pypdf/*.md`
- `markdown/nougat/*.md`

### 4. Generate Summaries

```bash
python summarize_papers.py
```

Outputs: `summaries/*.md`

## 📁 Project Structure

```plaintext
src/
├── config/
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── scholarly_client.py
│   ├── pdf_processor.py
│   └── llm_client.py
├── extractors/
│   ├── __init__.py
│   ├── base.py
│   ├── pypdf.py
│   └── nougat.py
├── chains/
│   ├── __init__.py
│   ├── paper_collection.py
│   ├── text_extraction.py
│   └── summarization.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py
│   └── async_utils.py
└── main.py
```

## 🔍 Output Formats

### Paper Collection (`papers.md`)

```markdown
| Title | Authors | Year | Citations | Link |
| ----- | ------- | ---- | --------- | ---- |
| ...   | ...     | ...  | ...       | ...  |
```

### Summaries Format

```markdown
1. Title
2. Key Points
3. Main Contributions
4. Methodology
5. Results and Conclusions
6. Future Work
```

## ⚠️ Limitations

- Some papers may be behind paywalls
- Download rates may be limited by sources
- PDF extraction quality varies
- API costs for summarization
- Network dependencies

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License

## 🙏 Acknowledgments

- [Thinking-Claude](https://github.com/richards199999/Thinking-Claude)
- [dblp-api](https://github.com/alumik/dblp-api)
