# AI-GlusterFs-Project

## Description:
This project (Flask Application) aims to create a chatbot system that utilizes GlusterFS for storing conversation logs. The chatbot will be designed to interact with users in natural language, providing simple responses to queries or engaging in conversations based on predefined knowledge or machine learning algorithms. The conversation data will be securely stored in a GlusterFS server, allowing for scalable and distributed storage solutions.

## Features
- **Web Interface**: Provides a user-friendly web interface powered by Flask for interacting with the chatbot.
- **Scalable Storage**: Implements GlusterFS for storing conversation logs, ensuring scalability and fault tolerance.
- **Customizable Responses**: Allows for easy customization of responses based on specific application or domain requirements.

## Installation
1. Clone the repository: `git clone https://github.com/zakia12ouajih/AI-GlusterFs-Project.git`
2. Install dependencies: `pip install -r flask`
3. Configure GlusterFS server details in app.py file change the mounting point in *save_chat_file* function.
4. Run the Flask application: `python app.py`

## Usage
1. Access the web interface provided by the Flask application.
2. Interact with the chatbot by sending messages or queries through the interface.
3. Conversation logs will be automatically saved to the configured GlusterFS server.

