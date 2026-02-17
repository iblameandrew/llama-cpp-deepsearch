# Local Deep Researcher

A **fully local**, **privacy-first** web research assistant that runs entirely on your machine. Give it a research topic and it will autonomously search the web, analyze sources, identify knowledge gaps, and iterate until it produces a comprehensive research report with citations.

**No data leaves your machine.** Everything runs locally using Ollama, LMStudio, llama-cpp-server, or optionally via OpenRouter for cloud models.

![Local Deep Researcher](https://github.com/user-attachments/assets/1c6b28f8-6b64-42ba-a491-1ab2875d50ea)

## Why Local Deep Researcher?

Most web research tools send your queries to external APIs, compromising privacy and incurring costs. This project enables:

- **100% Local Execution** - Your research queries never leave your machine
- **No API Costs** - Run unlimited research without paying for API calls
- **Full Privacy** - Sensitive research topics stay completely private
- **GPU-Accelerated** - Leverage your local GPU for fast inference
- **Simple GUI** - Easy-to-use Streamlit interface (no complex setup)

## Features

### Multiple LLM Providers
- **Ollama** - Run models like DeepSeek R1, Llama 3.2, Qwen locally
- **LMStudio** - Desktop app for loading various model formats
- **llama-cpp-server** - High-performance GGUF model serving
- **OpenRouter** - Cloud fallback with free tier options

### Multiple Search Backends
- **DuckDuckGo** - Free, no API key required
- **Tavily** - High-quality search results
- **Perplexity** - AI-powered search
- **SearXNG** - Self-hosted metasearch engine

### Research Capabilities
- Iterative research with configurable depth (1-10 loops)
- Automatic query generation and refinement
- Knowledge gap analysis and follow-up queries
- Source deduplication and citation
- Full page content fetching

## Quick Start

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/) **OR** [LMStudio](https://lmstudio.ai/) **OR** [llama.cpp](https://github.com/ggerganov/llama.cpp)

### Installation

```bash
git clone https://github.com/langchain-ai/local-deep-researcher.git
cd local-deep-researcher
pip install -e .
```

### Option 1: Streamlit GUI (Recommended)

The simplest way to use Local Deep Researcher:

```bash
streamlit run app.py
```

This opens a web interface where you can:
- Select your LLM provider and model
- Choose your search backend
- Set research depth
- View intermediate research steps in real-time

![Streamlit GUI](https://github.com/user-attachments/assets/02084902-f067-4658-9683-ff312cab7944)

### Option 2: LangGraph Studio

For advanced debugging and visualization:

```bash
# Install dependencies
pip install -e .
pip install -U "langgraph-cli[inmem]"

# Start the server
langgraph dev
```

Then open the LangGraph Studio URL in your browser.

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# LLM Provider: ollama, lmstudio, llama_cpp, openrouter
LLM_PROVIDER=ollama
LOCAL_LLM=llama3.2

# Provider-specific settings
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LLAMA_CPP_BASE_URL=http://127.0.0.1:8080/v1

# OpenRouter (optional cloud fallback)
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=stepfun/step-3.5-flash:free

# Search: tavily, perplexity, searxng
SEARCH_API=tavily
TAVILY_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
SEARXNG_URL=http://localhost:8888

# Research settings
MAX_WEB_RESEARCH_LOOPS=3
FETCH_FULL_PAGE=True
```

### Recommended Models

For best results with local research:

| Model | Provider | Size | Notes |
|-------|----------|------|-------|
| DeepSeek R1 7B | Ollama | 4.7GB | Excellent reasoning |
| Qwen 2.5 32B | LMStudio | ~20GB | Strong performance |
| Llama 3.2 3B | Ollama | 2GB | Fast, lightweight |
| Phi-4 | OpenRouter | Cloud | Free tier available |

## How It Works

The research agent follows an iterative loop:

```
1. Generate Search Query → 2. Web Search → 3. Summarize Findings
                                                        ↓
                              4. Identify Gaps ← 5. Reflect & Refine
```

1. **Query Generation** - Given your topic, generates an optimized search query
2. **Web Search** - Searches the web using your chosen backend
3. **Summarization** - Synthesizes findings into a coherent summary
4. **Reflection** - Analyzes the current knowledge for gaps
5. **Refinement** - Generates a new query to address gaps
6. **Repeat** - Continues for configured number of iterations

## Comparing to Alternatives

| Feature | Local Deep Researcher | Original LangChain | Perplexity |
|---------|----------------------|-------------------|------------|
| Runs locally | ✅ | ❌ | ❌ |
| No API costs | ✅ | ✅ | ❌ |
| GPU acceleration | ✅ | ✅ | ❌ |
| Streamlit GUI | ✅ | ❌ | N/A |
| Open source | ✅ | ✅ | ❌ |
| Privacy-first | ✅ | Partial | ❌ |

## Docker Deployment

```bash
# Build
docker build -t local-deep-researcher .

# Run (requires separate Ollama)
docker run --rm -it -p 2024:2024 \
  -e SEARCH_API=tavily \
  -e TAVILY_API_KEY=your_key \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  local-deep-researcher
```

## Video Tutorials

- [Overview with DeepSeek R1](https://www.youtube.com/watch?v=sGUjmyfof4Q)
- [Building from Scratch](https://www.youtube.com/watch?v=XGuTzHoqlj8)

## License

MIT

## Credits

Inspired by [IterDRAG](https://arxiv.org/html/2410.04343v1) and built with [LangGraph](https://langchain-ai.github.io/langgraph/).
