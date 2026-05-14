# Local-LLM-Assistant-Ollama 🤖

A private and offline AI assistant that runs entirely on your local machine. It uses the **Ollama** framework to serve models and Python for voice interaction.

## 🌟 Key Features
- **Privacy First:** No data leaves your machine; all AI processing is done locally.
- **Voice Commands:** Uses `speech_recognition` to listen to your instructions.
- **Customizable Models:** Easily switch between models like `Llama 3`, `Mistral`, or `Phi-3` via Ollama.
- **Local TTS:** Integrated with `pyttsx3` for offline text-to-speech.

## 🚀 Setup & Installation

1. **Install Ollama:**
   - Download and install Ollama from [ollama.com](https://ollama.com/).
   - Pull your preferred model (e.g., `ollama run llama3`).

2. **Clone & Install Dependencies:**
   ```bash
   pip install speech_recognition pyttsx3 requests
   
   Configure the Code:

Ensure your Ollama server is running (usually at http://localhost:11434).

Update the model name in your Python script if you are using something other than the default.

💻 Usage
Run the script and start talking to your local AI!

Python
python your_script_name.py

👨‍💻 Developer
NAVOJIT BAIDYA

CSE Student at Daffodil International University (DIU).

Passionate about AI Development & Cybersecurity.
