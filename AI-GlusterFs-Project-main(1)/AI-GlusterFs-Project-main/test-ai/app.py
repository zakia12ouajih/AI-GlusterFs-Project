from flask import Flask, render_template, request, jsonify
import os
import shutil
import subprocess
import re
import datetime
import long_responses as long  # Assuming this module exists
# Uncomment these imports if you plan to use them later
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

app = Flask(__name__)
initialized = False
current_log_file = None
# Initialize your model and tokenizer here if needed


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
   message_certainty = 0
   has_required_words = True

   for word in user_message:
      if word in recognised_words:
         message_certainty += 1

   percentage = float(message_certainty) / float(len(recognised_words))

   for word in required_words:
      if word not in user_message:
            has_required_words = False
            break

   if has_required_words or single_response:
        return int(percentage * 100)
   else:
      return 0


def check_all_messages(message):
   highest_prob_list = {}

   def response(bot_response, list_of_words, single_response=False, required_words=[]):
      nonlocal highest_prob_list
      highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

   response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
   response('See you!', ['bye', 'goodbye'], single_response=True)
   response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
   response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
   response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

   response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
   response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

   best_match = max(highest_prob_list, key=highest_prob_list.get)
   return long.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
   split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
   response = check_all_messages(split_message)
   return response


def initialize():
   global current_log_file
   global initialized
   if not initialized:
      # Generate a unique log file name based on the current timestamp
      current_log_file = f"chat_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
      initialized = True


@app.route('/')
def index():
   initialize()
   return render_template('chat.html')


@app.route('/get', methods=["POST"])
def chat():
   msg = request.form["msg"]
   response = get_response(msg)
   save_chat_file(msg, response)
   return response




def save_chat_file(user_message, bot_response):
    gluster_mount_point = "/mnt/glusterfs"
    if not os.path.exists(gluster_mount_point):
        raise FileNotFoundError("mount not found")
    
    with open(current_log_file, "a") as file:
        file.write(f"user: {user_message}\nBot: {bot_response}\n\n")
    
    # Use sudo programmatically to copy the file
    subprocess.run(['sudo', 'cp', current_log_file, gluster_mount_point], check=True)



if __name__ == '__main__':
   app.run(debug=True)
