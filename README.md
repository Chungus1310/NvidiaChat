# Nvidia AI Chat Interface

A modern Streamlit-based chat interface for interacting with various AI models through Nvidia's API platform.

## Features

- Support for multiple advanced language models:
  - Nemotron 4 340B
  - Yi Large
  - Mixtral 8x22B
  - Llama3 70B
  - Mistral Large 2
  - Codellama 70B
  - Llama3 ChatQA 70B
- Real-time streaming responses
- Adjustable model parameters
- Chat history export
- Custom system prompts
- Modern, responsive UI

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd nvidia
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variable:
```bash
# Linux/Mac
export nv_token="your-api-key-here"

# Windows (Command Prompt)
set nv_token=your-api-key-here

# Windows (PowerShell)
$env:nv_token="your-api-key-here"
```

4. Run the application:
```bash
streamlit run nv.py
```

## Usage

1. Select a model from the dropdown menu
2. Adjust parameters if needed:
   - Temperature (default: 0.3)
   - Top P (default: 0.95)
   - Max Tokens (default: 1024)
3. Enter your message in the chat input
4. View the streaming response
5. Export chat history as needed

## Configuration

- Default temperature: 0.3
- Default top_p: 0.95
- Max tokens range: 100-2000
- System prompt: Customizable via sidebar

## Requirements

- Python 3.8+
- OpenAI Python SDK
- Streamlit
- Valid Nvidia API key

## License

MIT License

## Author

Chun

## Acknowledgments

Powered by Nvidia AI Platform
