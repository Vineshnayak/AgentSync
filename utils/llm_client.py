import time
import re
from typing import List, Optional, Callable, Any
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from config.settings import settings
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("llm_client")

def get_chat_llm(max_retries: int = 4, request_timeout: int = 30) -> ChatGroq:
    """Returns a ChatGroq instance configured with resilient retry settings."""
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.DEFAULT_MODEL,
        max_retries=max_retries,
        request_timeout=request_timeout
    )

def sanitize_error(err: Exception) -> str:
    """Sanitizes raw LLM/system errors so that no internal backend plumbing,
    model names, org IDs, TPM limits, or billing URLs are exposed to the frontend.
    """
    err_str = str(err)
    if any(k in err_str.lower() for k in ["429", "rate_limit", "tpm", "tokens per minute", "groq", "billing"]):
        return "High Operational Traffic: System automatically applied in-process fallback heuristics."
    if any(k in err_str.lower() for k in ["timeout", "timed out"]):
        return "Operational Latency: Diagnostic engine completed triage using fallback evaluation."
    # Strip any leaked model IDs or org keys
    cleaned = re.sub(r'openai/[a-zA-Z0-9\-_]+', 'AI Reasoning Engine', err_str)
    cleaned = re.sub(r'org_[a-zA-Z0-9]+', '***', cleaned)
    cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
    return cleaned

def invoke_with_retry(
    llm: ChatGroq,
    messages: List[BaseMessage],
    fallback_generator: Optional[Callable[[], str]] = None,
    max_retries: int = 3
) -> str:
    """Invokes the ChatGroq model with proactive handling of 429 rate limits.
    If rate-limited, parses the required sleep time and retries up to max_retries.
    If all retries fail, invokes fallback_generator() if provided.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            logger.info(f"Invoking LLM (attempt {attempt + 1}/{max_retries})...")
            response = llm.invoke(messages)
            global_metrics.increment_llm()
            return response.content
        except Exception as e:
            err_msg = str(e)
            attempt += 1
            is_rate_limit = "429" in err_msg or "rate_limit" in err_msg.lower() or "tpm" in err_msg.lower()
            
            if is_rate_limit and attempt < max_retries:
                # Extract wait time if present, e.g. "try again in 2.4375s"
                wait_match = re.search(r'try again in (\d+(\.\d+)?)s', err_msg, re.IGNORECASE)
                wait_seconds = float(wait_match.group(1)) + 0.5 if wait_match else (2.0 * attempt + 1.0)
                logger.warning(f"Rate limit encountered. Sleeping for {wait_seconds:.2f}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_seconds)
            else:
                logger.error(f"LLM invocation failed on attempt {attempt}: {err_msg}")
                if attempt >= max_retries:
                    break
                time.sleep(1.5)

    if fallback_generator:
        logger.info("Invoking automated in-process fallback heuristic...")
        return fallback_generator()
        
    raise RuntimeError(sanitize_error(Exception("LLM reasoning service temporarily unavailable.")))
