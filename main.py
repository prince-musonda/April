from ollama import chat
from tts import text_to_speech_stream
import threading
import os
import json

memory_and_soul  =  "./memory_and_soul"
os.makedirs(memory_and_soul,exist_ok=True )

def get_memory_path():
    return os.path.join(memory_and_soul,"memory.jsonl")

def load_memory():
    "load conversation history"
    path = get_memory_path()
    messages = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                # check if it is just white space
                if line.strip():
                    messages.append(json.loads(line))
    return messages


def get_soul_path():
    return os.path.join(memory_and_soul, "soul.md")

def load_soul():
    pass

def append_to_memory(message):
    "add a single message to memory"
    path = get_memory_path()
    with open(path, "a") as f:
        f.write(json.dumps(message) + "\n")



def main():
    # load memory
    messages =  load_memory()
    while True:
        users_message = input("me: ")
        users_message = {'role': "user", "content": users_message}
        messages.append(users_message)
        append_to_memory(users_message)
        stream = chat(
            model = 'gemma4:e4b',
            messages = messages,
            think = False,
            stream = True,
            options ={
            'temperature': 0.1,      # Forces 'straight-line' logic (Fast)
            'top_p': 0.9,            # Limits word choices to the most relevant
            'repeat_penalty': 1.2    # Prevents him from repeating "Let me think...
            }
        )

        response = ''
        done_thinking = True
        for chunk in stream:
            thinking = chunk['message'].get('thinking')
            responding = chunk['message'].get('content')
            if thinking:
                print(chunk['message']['thinking'],end='',flush=True)
            elif responding:
                if done_thinking:
                    # separate thoughts from response by a line 
                    print('\n')
                    done_thinking = False
                response += chunk['message']['content']
                print(chunk['message']['content'], end='', flush=True)
                audio_stream = text_to_speech_stream(chunk['message']['content'])
                # i play the audio in a different stream here
        assistants_message = {"role":'assistant', 'content': response}
        messages.append(assistants_message)
        append_to_memory(assistants_message)
        print("\n")
        


if __name__ == "__main__":
    main()