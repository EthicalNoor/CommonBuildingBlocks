# CommonBuildingBlocks\AI_Innovation_Hub\tts_gateway\tts_configurator.py

TTS_CONFIG = {
    "GoogleTTS": {
        "version": "google.text-to-speech-v1",
        "language_code":"en-US",
        "voice_name":"en-US-Standard-C",
        "ssml_gender":"FEMALE",
        "max_text_length": 5000,
        "invocation_type": "GoogleTTSModel"
    },
    "ElevenLabsTTS": {
        "model": "eleven_multilingual_v1",
        "invocation_type": "ElevenLabsTTSModel",
    },
    "FastAPITTS": {
        "version": "fastapi.tts-v1",
        "fastapi_url": "https://a208-34-75-176-82.ngrok-free.app/speak",  # update as needed
        "language": "en",
        "emotion": "neutral",  # Default; can be overridden as required
        "invocation_type": "FastAPITTSModel"
    },
    "GTTS": {
        "version": "gtts-v1",
        "max_text_length": 5000,
        "language": "en",
        "emotion": "neutral",  # Default; modify if needed (e.g., "sad" to slow down)
        "invocation_type": "GTTSModel"
    }
}
