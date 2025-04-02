# CommonBuildingBlocks\AI_Innovation_Hub\stt_gateway\stt_configurator.py

STT_CONFIG = {
    "AssemblyAI_STT": {
        "version": "assemblyai.stt-v1",
        "max_audio_length": 7200,
        "input_audio_limit_ms": 48000,
        "invocation_type": "AssemblyAISTTModel"
    },
    "Deepgram": {
        "version": "latest",
        "model":"nova-2-general",
        "invocation_type": "DeepgramSTTModel",
        "language":"en-US"
    },   
    "OpenAI_Whisper_Local": {
        "version": "openai.whisper",
        "max_audio_length": 7200,
        "input_audio_limit_ms": 48000,
        "invocation_type": "LocalSTTModel",
        "model": "base"
    },
    "CoquiSTT": {
        "version": "coqui.stt-v1",
        "max_audio_length": 3600,
        "input_audio_limit_ms": 48000,
        "invocation_type": "CoquiSTTModel"
    },
    "Wav2vecSTT": {
        "version": "wav2vec.stt",
        "max_audio_length": 3600,
        "input_audio_limit_ms": 48000,
        "invocation_type": "OpenSource"
    }
}
