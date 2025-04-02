# AI_Innovation_Hub\llm_gateway\llm_configurator.py

LLM_CONFIG = {
    "GroqLLM": {
        "version": "llama3-8b-8192",
        "input_token_limit": 8000,           
        "invocation_type": "GroqLLMModel",   
        "bedrock_supported": False,          
        "GROQ_MODEL": "llama3-8b-8192",
        "max_tokens": 1000,                  
        "temperature": 0.9                  
    },
    "GPT-4o": {
        "version": "gpt-4o",
        "input_token_limit": 128000,
        "invocation_type": "OpenAIModel",
        "bedrock_supported": "No"
    },
    "Gemini Flash 1.5": {
        "version": "gemini-1.5-flash",
        "input_token_limit": 1048576,
        "invocation_type": "GeminiModel",
        "bedrock_supported": "No"
    },
    "Mistral-7b": {
        "version": "mistral.mistral-7b-instruct-v0:2",
        "input_token_limit": 32000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "Mistral-8x7b": {
        "version": "mistral.mistral-8x7b-instruct-v0:1",
        "input_token_limit": 32000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "Mistral-Large": {
        "version": "mistral.mistral-large-2402-v1:0",
        "input_token_limit": 32000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "anthropic.claude-3-sonnet": {
        "version": "anthropic.claude-3-sonnet",
        "input_token_limit": 28000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "anthropic.claude-3-haiku": {
        "version": "anthropic.claude-3-haiku-20240307-v1:0",
        "input_token_limit": 48000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "meta.llama3-8b-instruct-v1:0": {
        "version": "meta.llama3-8b-instruct-v1:0",
        "input_token_limit": 8000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    },
    "meta.llama3-70b-instruct-v1:0": {
        "version": "meta.llama3-70b-instruct-v1:0",
        "input_token_limit": 8000,
        "invocation_type": "ChatRockLLMModel",
        "bedrock_supported": "Yes",
        "AWS_REGION":"us-west-2" #new update
    }
}
