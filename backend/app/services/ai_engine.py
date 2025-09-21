import os
from enum import Enum
from ..core.security import get_api_key
from ..core.prompt_library import get_cv_optimization_prompt, get_cover_letter_prompt

# (Placeholder) Import actual client libraries when implementing fully
# import openai
# import google.generativeai as genai
# import anthropic

class AITaskType(Enum):
    """Defines the type of task for the AI to perform, influencing model selection."""
    ANALYSIS = "analysis"  # For tasks like keyword extraction, matching
    CREATIVE_WRITING = "creative_writing"  # For tasks like cover letter generation
    GENERAL = "general"  # For balanced, general-purpose tasks

class AIModelProvider(Enum):
    """Defines the AI provider to use."""
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"

def _call_openai(prompt: str, model: str) -> str:
    """Placeholder for calling the OpenAI API."""
    api_key = get_api_key(AIModelProvider.OPENAI.value)
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set it in the settings.")
    # client = openai.OpenAI(api_key=api_key)
    # response = client.chat.completions.create(...)
    print(f"--- FAKE OPENAI CALL --- \nModel: {model}\nPrompt: {prompt[:100]}...\n--- END FAKE CALL ---")
    return f"Fake response from OpenAI model {model} for prompt: '{prompt[:50]}...'"

def _call_google(prompt: str, model: str) -> str:
    """Placeholder for calling the Google Gemini API."""
    api_key = get_api_key(AIModelProvider.GOOGLE.value)
    if not api_key:
        raise ValueError("Google API key not found. Please set it in the settings.")
    # genai.configure(api_key=api_key)
    # model = genai.GenerativeModel(model)
    # response = model.generate_content(...)
    print(f"--- FAKE GOOGLE CALL --- \nModel: {model}\nPrompt: {prompt[:100]}...\n--- END FAKE CALL ---")
    return f"Fake response from Google model {model} for prompt: '{prompt[:50]}...'"

def _call_anthropic(prompt: str, model: str) -> str:
    """Placeholder for calling the Anthropic Claude API."""
    api_key = get_api_key(AIModelProvider.ANTHROPIC.value)
    if not api_key:
        raise ValueError("Anthropic API key not found. Please set it in the settings.")
    # client = anthropic.Anthropic(api_key=api_key)
    # response = client.messages.create(...)
    print(f"--- FAKE ANTHROPIC CALL --- \nModel: {model}\nPrompt: {prompt[:100]}...\n--- END FAKE CALL ---")
    return f"Fake response from Anthropic model {model} for prompt: '{prompt[:50]}...'"


def get_ai_response(prompt: str, task_type: AITaskType) -> str:
    """
    Routes a request to the appropriate LLM based on the task type.

    This is the core "AI Router" logic.
    """
    print(f"Routing AI request for task type: {task_type.value}")

    if task_type == AITaskType.ANALYSIS:
        # Use a fast and cheap model for analysis.
        # As per prompt, GPT-4o mini or Gemini 2.0 Flash. Let's use Gemini.
        model = "gemini-2.0-flash"
        return _call_google(prompt, model)

    elif task_type == AITaskType.CREATIVE_WRITING:
        # Use a high-quality model for creative tasks.
        # As per prompt, Claude Sonnet 4.
        model = "claude-4-sonnet"
        return _call_anthropic(prompt, model)

    elif task_type == AITaskType.GENERAL:
        # Use a balanced, powerful model for general tasks.
        # As per prompt, GPT-4o or Gemini 2.5 Pro. Let's use GPT-4o.
        model = "gpt-4o"
        return _call_openai(prompt, model)

    else:
        raise ValueError(f"Unknown AI task type: {task_type}")

# Example of how this might be used with the prompt library
def generate_optimized_cv_content(job_description: str, user_cv: str) -> str:
    """
    Generates optimized CV content based on a job description.
    """
    prompt = get_cv_optimization_prompt(job_description, user_cv)
    # CV optimization is a mix of analysis and writing, let's use the General model
    return get_ai_response(prompt, AITaskType.GENERAL)

def generate_cover_letter_content(job_description: str, user_cv: str, company_mission: str = "") -> str:
    """
    Generates a personalized cover letter.
    """
    prompt = get_cover_letter_prompt(job_description, user_cv, company_mission)
    # Cover letter is a creative task
    return get_ai_response(prompt, AITaskType.CREATIVE_WRITING)
