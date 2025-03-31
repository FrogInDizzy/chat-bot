# chat-bot
Overview
The Intelligent Chatbot Suite is a robust and scalable chatbot system designed to handle automated conversations using Feishu (Lark) API and GPT-powered AI responses. It integrates multiple components, including message handling, API interactions, and response generation, making it suitable for enterprise and personal chatbot applications.

This suite provides:

Feishu (Lark) Message Handling: Process and reply to messages from Feishu users.
AI-Powered Responses: Uses GPT models (e.g., gpt-3.5-turbo) for intelligent chatbot responses.
Configurable Message Cards: Dynamically update chat settings using interactive message cards.
Asynchronous Processing: Ensures efficient and responsive communication.
Features
🚀 Feishu Chatbot Integration
Receives messages from Feishu users.
Supports text, images, and interactive card messages.
Utilizes Feishu OpenAPI for authentication and messaging.
🤖 AI-Powered Response System
Uses GPT-3.5-Turbo (configurable) for generating intelligent responses.
Supports customizable temperature settings for response creativity.
Retries failed API calls with automatic token refreshing.
🔄 Dynamic Configuration Management
Uses interactive message cards to allow users to change chatbot settings on the fly.
Stores user preferences, including model choice and chat settings.
⏳ Robust Error Handling & Logging
Implements retry mechanisms for failed API requests.
Logs all chatbot interactions for debugging and analytics.
Project Structure
📂 intelligent-chatbot-suite
 ├── app_relevant/                 # Core chatbot functionalities
 │   ├── lark_msg_sender.py        # Sends replies via Feishu API
 │   ├── one_api_answer.py         # Handles AI responses from GPT
 │   ├── push_card_msg.py          # Manages interactive cards in Feishu
 │   ├── token_manager.py          # Manages authentication tokens
 ├── config/                       # Configuration management
 │   ├── fetch_config_by_ip.py     # Fetches API credentials dynamically
 ├── public_library/               # Utility functions and libraries
 │   ├── utils/
 │   │   ├── dotmap_cus.py         # JSON-like object manipulation
 │   │   ├── json_util.py          # JSON file operations
 │   │   ├── logger_wall.py        # Logging utilities
 ├── constants/                     # Stores general configurations
 ├── setting.py                     # Project-wide settings
 ├── main.py                         # Entry point for chatbot operation
 ├── README.md                       # Documentation
Installation
Prerequisites
Python 3.7+
pip install -r requirements.txt
Feishu Developer Account
OpenAI API Key (or alternative LLM API)
Setup
Clone the repository
git clone https://github.com/yourusername/intelligent-chatbot-suite.git
cd intelligent-chatbot-suite
Install dependencies
pip install -r requirements.txt
Set up environment variables
export APP_ID='your_feishu_app_id'
export APP_SECRET='your_feishu_app_secret'
export GPT_API_KEY='your_openai_api_key'
Run the chatbot
python main.py
Usage
1️⃣ Sending Messages to the Chatbot
The chatbot listens for messages on Feishu.
Replies using GPT-generated text.
Can be configured to respond differently based on user settings.
2️⃣ Updating Chatbot Configuration
Users can send a custom interactive card to update settings like:
AI model (e.g., GPT-3.5-Turbo, GPT-4)
Temperature (response randomness)
Chat mode (QA, conversational, creative, etc.)
3️⃣ Handling Authentication and Tokens
TokenManager automatically refreshes tokens upon expiration.
Secure API requests using Bearer Token Authentication.
Extending the Project
🔧 Adding New AI Models
Modify one_api_answer.py:

"model_name": "gpt-4"
🎨 Customizing Response Behavior
Update reply_message in main.py:

qq = {
    "question": user_text,
    "model_name": "gpt-4",
    "temperature": 0.7,
    "chat_mode": "creative",
}
📌 Adding More Message Types
Modify lark_msg_sender.py to handle images, attachments, or buttons.

Troubleshooting
❓ Bot Not Responding
Check Feishu webhook and credentials.
Verify logs in logs/ directory.
🔄 Token Expired
Restart the bot (python main.py).
Ensure TokenManager is correctly refreshing tokens.
Contributing
Feel free to open issues and pull requests. Contributions are welcome! 🚀

License
MIT License © 2025 Dragon