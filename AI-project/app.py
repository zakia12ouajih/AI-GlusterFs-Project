from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import datetime

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Create a Flask application instance
app = Flask(__name__)

current_log_file = None
initialized = False



def initialize():
   global current_log_file
   # Generate a unique log file name based on the current timestamp
   current_log_file = f"chat_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"


# Define a route and a function to handle requests to that route
@app.route('/')
def index():
   global initialized
   if not initialized:
      initialize()
      initialized = True
   return render_template('chat.html')


@app.route('/get', methods={"GET","POST"})
def chat():
   msg = request.form["msg"]
   input = msg
   response = get_chat_response(msg)
   save_chat_file(msg, response)
   return response



def get_chat_response(text):
# Let's chat for 5 lines
   for step in range(5):
   # encode the new user input, add the eos_token and return a tensor in Pytorch
      new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

      # append the new user input tokens to the chat history
      bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

      # generated a response while limiting the total chat history to 1000 tokens, 
      chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

      # pretty print last ouput tokens from bot
      return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

def save_chat_file(user_message, bot_response):
   with open(current_log_file, "a") as file:
      file.write(f"User: {user_message}\nBot: {bot_response}\n\n")


# Run the Flask application
if __name__ == '__main__':
   app.run(debug=True)
