import json
import os
import streamlit as st
from pathlib import Path
from typing import Any

CONFIG_FILE = Path.home() / ".local-deep-researcher" / "config.json"


def ensure_config_dir() -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_config(config: dict[str, Any]) -> None:
    ensure_config_dir()
    existing = load_config()
    existing.update(config)
    with open(CONFIG_FILE, "w") as f:
        json.dump(existing, f, indent=2)


def get_config_value(key: str, default: Any = None) -> Any:
    if key in st.session_state:
        return st.session_state[key]
    saved = load_config()
    return saved.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    st.session_state[key] = value
    save_config({key: value})


def main():
    st.set_page_config(
        page_title="Local Deep Researcher", page_icon="🔍", layout="wide"
    )

    st.title("🔍 Local Deep Researcher")
    st.markdown("A fully local web research assistant using LLMs")

    with st.sidebar:
        st.header("⚙️ Configuration")

        llm_provider = st.selectbox(
            "LLM Provider",
            ["ollama", "lmstudio", "llama_cpp", "openrouter"],
            index=["ollama", "lmstudio", "llama_cpp", "openrouter"].index(
                get_config_value("llm_provider", "ollama")
            ),
        )
        set_config_value("llm_provider", llm_provider)

        local_llm = st.text_input(
            "Model Name", value=get_config_value("local_llm", "llama3.2")
        )
        set_config_value("local_llm", local_llm)

        if llm_provider == "ollama":
            ollama_base_url = st.text_input(
                "Ollama Base URL",
                value=get_config_value("ollama_base_url", "http://localhost:11434/"),
            )
            set_config_value("ollama_base_url", ollama_base_url)
        elif llm_provider == "lmstudio":
            lmstudio_base_url = st.text_input(
                "LMStudio Base URL",
                value=get_config_value("lmstudio_base_url", "http://localhost:1234/v1"),
            )
            set_config_value("lmstudio_base_url", lmstudio_base_url)
        elif llm_provider == "llama_cpp":
            llama_cpp_base_url = st.text_input(
                "llama-cpp Base URL",
                value=get_config_value(
                    "llama_cpp_base_url", "http://127.0.0.1:8080/v1"
                ),
            )
            set_config_value("llama_cpp_base_url", llama_cpp_base_url)
        elif llm_provider == "openrouter":
            openrouter_api_key = st.text_input(
                "OpenRouter API Key",
                type="password",
                value=get_config_value("openrouter_api_key", ""),
            )
            set_config_value("openrouter_api_key", openrouter_api_key)
            openrouter_model = st.text_input(
                "OpenRouter Model",
                value=get_config_value(
                    "openrouter_model", "stepfun/step-3.5-flash:free"
                ),
            )
            set_config_value("openrouter_model", openrouter_model)

        st.divider()
        st.subheader("🔎 Search Settings")

        search_api = st.selectbox(
            "Search API",
            ["tavily", "perplexity", "searxng"],
            index=["tavily", "perplexity", "searxng"].index(
                get_config_value("search_api", "tavily")
            ),
        )
        set_config_value("search_api", search_api)

        if search_api == "tavily":
            tavily_api_key = st.text_input(
                "Tavily API Key",
                type="password",
                value=get_config_value("tavily_api_key", ""),
            )
            set_config_value("tavily_api_key", tavily_api_key)
        elif search_api == "perplexity":
            perplexity_api_key = st.text_input(
                "Perplexity API Key",
                type="password",
                value=get_config_value("perplexity_api_key", ""),
            )
            set_config_value("perplexity_api_key", perplexity_api_key)
        elif search_api == "searxng":
            searxng_url = st.text_input(
                "SearXNG URL", value=get_config_value("searxng_url", "")
            )
            set_config_value("searxng_url", searxng_url)

        max_loops = st.slider(
            "Research Depth",
            min_value=1,
            max_value=50,
            value=get_config_value("max_web_research_loops", 3),
        )
        set_config_value("max_web_research_loops", max_loops)

        fetch_full_page = st.checkbox(
            "Fetch Full Page Content", value=get_config_value("fetch_full_page", True)
        )
        set_config_value("fetch_full_page", fetch_full_page)
        use_tool_calling = st.checkbox(
            "Use Tool Calling", value=get_config_value("use_tool_calling", False)
        )
        set_config_value("use_tool_calling", use_tool_calling)
        strip_thinking = st.checkbox(
            "Strip Thinking Tokens",
            value=get_config_value("strip_thinking_tokens", True),
        )
        set_config_value("strip_thinking_tokens", strip_thinking)

        st.divider()
        st.caption("Settings saved to ~/.local-deep-researcher/config.json")

    research_topic = st.text_area(
        "Enter your research topic:",
        height=100,
        placeholder="e.g., What are the latest developments in quantum computing?",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        start_button = st.button(
            "🚀 Start Research", type="primary", use_container_width=True
        )
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.research_result = None
            st.session_state.research_status = None
            st.session_state.research_steps = []
            st.session_state.progress_message = ""
            st.rerun()

    for key in [
        "research_result",
        "research_status",
        "research_steps",
        "current_topic",
        "current_config",
        "progress_message",
    ]:
        if key not in st.session_state:
            st.session_state[key] = None if key != "research_steps" else []

    if start_button and research_topic:
        config = {
            "configurable": {
                "llm_provider": get_config_value("llm_provider"),
                "local_llm": get_config_value("local_llm"),
                "search_api": get_config_value("search_api"),
                "max_web_research_loops": get_config_value("max_web_research_loops"),
                "fetch_full_page": get_config_value("fetch_full_page"),
                "use_tool_calling": get_config_value("use_tool_calling"),
                "strip_thinking_tokens": get_config_value("strip_thinking_tokens"),
                "ollama_base_url": get_config_value(
                    "ollama_base_url", "http://localhost:11434/"
                ),
                "lmstudio_base_url": get_config_value(
                    "lmstudio_base_url", "http://localhost:1234/v1"
                ),
                "llama_cpp_base_url": get_config_value(
                    "llama_cpp_base_url", "http://127.0.0.1:8080/v1"
                ),
                "openrouter_api_key": get_config_value("openrouter_api_key", ""),
                "openrouter_model": get_config_value(
                    "openrouter_model", "stepfun/step-3.5-flash:free"
                ),
                "tavily_api_key": get_config_value("tavily_api_key", ""),
                "perplexity_api_key": get_config_value("perplexity_api_key", ""),
                "searxng_url": get_config_value("searxng_url", ""),
            }
        }

        if get_config_value("tavily_api_key"):
            os.environ["TAVILY_API_KEY"] = get_config_value("tavily_api_key")
        if get_config_value("perplexity_api_key"):
            os.environ["PERPLEXITY_API_KEY"] = get_config_value("perplexity_api_key")
        if get_config_value("searxng_url"):
            os.environ["SEARXNG_URL"] = get_config_value("searxng_url")

        st.session_state.research_status = "running"
        st.session_state.research_steps = []
        st.session_state.progress_message = "Starting research..."
        st.session_state.current_topic = research_topic
        st.session_state.current_config = config

    if st.session_state.get("research_status") == "running":
        progress_placeholder = st.empty()

        progress_placeholder.info(
            f"🔄 {st.session_state.get('progress_message', 'Research in progress...')}"
        )

        from ollama_deep_researcher.graph import graph

        try:
            steps = []
            final_result = {}

            for chunk in graph.stream(
                {"research_topic": st.session_state.current_topic},
                config=st.session_state.current_config,
            ):
                if "generate_query" in chunk:
                    data = chunk["generate_query"]
                    st.session_state.progress_message = "🔍 Generating search query..."
                    progress_placeholder.info("🔍 Generating search query...")
                    steps.append(
                        {
                            "stage": "generate_query",
                            "title": "🔍 Generating Search Query",
                            "thinking": data.get("current_thinking", ""),
                            "query": data.get("search_query", ""),
                        }
                    )

                elif "web_research" in chunk:
                    data = chunk["web_research"]
                    query = data.get("last_search_query", "")
                    st.session_state.progress_message = f"🌐 Searching: {query}"
                    progress_placeholder.info(f"🌐 Searching: {query}")
                    steps.append(
                        {
                            "stage": "web_research",
                            "title": f"🌐 Web Search (Loop {data.get('research_loop_count', 0)})",
                            "thinking": data.get("current_thinking", ""),
                            "query": query,
                            "sources": data.get("last_sources", ""),
                        }
                    )

                elif "summarize_sources" in chunk:
                    data = chunk["summarize_sources"]
                    st.session_state.progress_message = "📝 Summarizing sources..."
                    progress_placeholder.info("📝 Summarizing sources...")
                    steps.append(
                        {
                            "stage": "summarize_sources",
                            "title": "📝 Summarizing Sources",
                            "thinking": data.get("current_thinking", ""),
                            "summary": data.get("running_summary", ""),
                        }
                    )

                elif "reflect_on_summary" in chunk:
                    data = chunk["reflect_on_summary"]
                    st.session_state.progress_message = (
                        "🧠 Reflecting on knowledge gaps..."
                    )
                    progress_placeholder.info("🧠 Reflecting on knowledge gaps...")
                    steps.append(
                        {
                            "stage": "reflect_on_summary",
                            "title": "🧠 Reflecting on Knowledge Gaps",
                            "thinking": data.get("current_thinking", ""),
                            "query": data.get("search_query", ""),
                        }
                    )

                elif "finalize_summary" in chunk:
                    final_result = chunk["finalize_summary"]

                st.session_state.research_steps = steps

            st.session_state.research_result = final_result
            st.session_state.research_status = "complete"
            progress_placeholder.success("✅ Research Complete!")

        except Exception as e:
            st.session_state.research_status = "error"
            st.session_state.error_message = str(e)
            progress_placeholder.error(f"❌ Error: {str(e)}")

        st.rerun()

    elif st.session_state.get("research_status") == "error":
        st.error(f"Error: {st.session_state.get('error_message', 'Unknown error')}")

    elif st.session_state.get("research_status") == "complete":
        st.success("✅ Research Complete!", icon="🎉")

        steps = st.session_state.get("research_steps", [])

        for i, step in enumerate(steps):
            with st.expander(f"{step['title']} (Step {i + 1})", expanded=True):
                if step.get("thinking"):
                    st.info(f"**Thinking:** {step['thinking']}")
                if step.get("query"):
                    st.markdown(f"**Query:** `{step['query']}`")
                if step.get("sources"):
                    st.markdown("**Sources:**")
                    st.code(
                        step["sources"][:5000] + "..."
                        if len(step["sources"]) > 5000
                        else step["sources"]
                    )
                if step.get("summary"):
                    st.markdown("**Summary:**")
                    st.markdown(
                        step["summary"][:3000] + "..."
                        if len(step["summary"]) > 3000
                        else step["summary"]
                    )

        result = st.session_state.research_result or {}
        summary = result.get("running_summary", "")
        if summary:
            st.markdown("---")
            st.markdown("## Final Report")
            st.markdown(summary)


if __name__ == "__main__":
    main()
