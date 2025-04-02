# EthicalGenAI - Common Building Blocks

This repository serves as the core framework for integrating various AI services. It includes a dedicated submodule that provides shared utilities, ensuring consistent functionality across all AI components. The design emphasizes modularity and scalability, enabling rapid integration and testing of diverse AI capabilities.

---

## Modules

- **Database Module**  
  Manages data storage, connection protocols, and schema definitions to ensure robust data handling.

- **Embeddings Module**  
  Provides mechanisms for generating and managing embeddings using various AI providers. It abstracts the integration details so that multiple embedding services can be used interchangeably.

- **Language Module**  
  Focuses on language detection and processing. It automatically identifies and processes text based on linguistic features, streamlining further operations.

- **LLM Integration Module**  
  Acts as the interface for interacting with large language models. This module supports integration with several LLM providers, allowing for flexible deployment of AI language services.

- **Queue Management**  
  Handles message queuing to streamline communication between different services. It ensures reliable and efficient processing of asynchronous tasks.

- **Storage Module**  
  Provides secure storage solutions and abstracts complex data storage requirements behind a unified interface.

- **Speech-to-Text Module**  
  Converts spoken language into text. This module integrates with state-of-the-art speech recognition services to ensure high accuracy.

- **Text-to-Speech Module**  
  Transforms textual content into natural-sounding speech. It leverages multiple service providers to generate high-quality audio output.

- **Text Refinement Module**  
  Refines and optimizes textual data. It processes raw text to produce a polished version, ready for downstream tasks.

- **Text Splitting Module**  
  Efficiently splits large bodies of text into manageable segments. This is crucial for processing lengthy content in iterative stages.

---

## Git Submodule Management

This project leverages a Git submodule to integrate common AI utilities. Below are the instructions to manage the submodule effectively:

### **Adding the Submodule**

To include the submodule in your repository, execute:

```bash
git submodule add https://github.com/EthicalNoor/CommonBuildingBlocks.git CommonBuildingBlocks

```

---

### **Initializing and Fetching the Submodule**

After cloning the main repository, initialize and fetch the submodule using the following commands:

```bash
git submodule init
git submodule update --init --recursive
```

This setup ensures that the submodule is correctly configured and all dependencies are loaded recursively.

---

### **Updating the Submodule**

To update the submodule with the latest changes from its remote source, run:

```bash
git submodule update --remote --merge
```

This command fetches the latest commits from the submodule's tracked branch and merges them into your current setup.

---

### **Committing Submodule Changes**

If the submodule has been updated, commit its changes in your main repository with:

```bash
git add CommonBuildingBlocks
git commit -m "Update submodule to latest version"
```

> **Tip:** Always verify the status of your submodule before committing to ensure that all changes are intentional.

---

Sensitive configurations, such as API keys and endpoints, are stored in environment configuration files. It is essential to keep these files secure and avoid committing them to public repositories. Consider using a dedicated secrets manager or environment variables to handle this sensitive data.

Example content for an environment configuration file:

```dotenv
# GROQ API configuration
GROQ_API_KEY="sample_groq_api_key"
GROQ_API_URL="https://sample.api.groq.com/v1"

# Google API configuration
GOOGLE_API_KEY="sample_google_api_key"

# Deepgram API configuration
DEEPGRAM_API_KEY="sample_deepgram_api_key"

# ElevenLabs API configuration
ELEVENLABS_VOICE_ID="sample_elevenlabs_voice_id"
ELEVENLABS_API_KEY="sample_elevenlabs_api_key"
```

> **Security Reminder:** Always restrict the permissions of your API keys and avoid exposing them in publicly accessible code.

---