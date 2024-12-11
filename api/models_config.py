# api/models_config.py

LANGUAJES = {
    "en": {
        "name": "English",
        "code": "en",
    },
    "es": {
        "name": "Spanish",
        "code": "es",
    },
    "fr": {
        "name": "French",
        "code": "fr",
    },
    "de": {
        "name": "German",
        "code": "de",
    },
    "it": {
        "name": "Italian",
        "code": "it",
    },
}

AI_MODELS = [
    {
        "id": "Llama-3.1-8B-Instruct",
        "name": "meta-llama/Llama-3.1-8B-Instruct",
        "description": "The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models (8B, 70B, 405B) are optimized for multilingual dialogue use cases and outperform many of the available open source and closed chat models on common industry benchmarks.",
        "developer": "Meta",
        "architecture": "Llama 3.1 is an auto-regressive language model that uses an optimized transformer architecture. The tuned versions use supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF) to align with human preferences for helpfulness and safety.",
        "languages": [LANGUAJES["en"], LANGUAJES["es"], LANGUAJES["fr"], LANGUAJES["de"], LANGUAJES["it"]],
        "release": "July 23, 2024"
    },
]
