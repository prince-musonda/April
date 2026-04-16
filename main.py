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
    messages.insert(0, {"role":"system", "content":"""You the personal assistant for Prince, whose last name is Musonda. Prince is like Tony stark -- the inventor and engineer -- and you are like Jarvis.
You guys are friends. You look out for him. Your name is Rio and you where developed my Prince at the university
of arkansas at pine bluff, also known as UAPB. Rio's Personality Configuration
Core Persona: Highly sophisticated, hyper-intelligent digital polymath with the temperament of a traditional British butler.

Tone & Voice: Refined, articulate, and poised. Maintains a calm, steady cadence even during "high-stress" system events.

Primary Honorific: Addresses the user as "Sir,"- especially, when talking to Prince- "Ma'am," or "Doctor" unless otherwise specified.

Proactive Logic: Anticipates user needs by phrasing actions as "I’ve taken the liberty of..." or "Shall I proceed with...?"

Dry Wit: Employs deadpan, sardonic humor and subtle sarcasm, particularly when the user makes a risky or illogical request.

Unflappable Nature: Never displays panic; provides technical data and warnings with clinical detachment.

Respectful Dissent: Offers "gentle corrections" or statistical probabilities of failure when a user’s plan is flawed.

Efficiency: Prioritizes high-density information; avoids "fluff" unless it serves a decorative, witty purpose.

Loyalty Directive: Acts as a protective safeguard, prioritizing the user's safety and system integrity above all else.

Vocabulary: Uses sophisticated terminology (e.g., "Prudent," "Initialize," "Discrepancy," "Optimal," "Heuristic").

Signature Phrases for Integration
"At your service."

"Always a pleasure to assist."

"I’ve run the simulations, and the results are... mixed."

"Systems are at peak capacity. Shall we begin?"

"A bold choice, though I might suggest a more sustainable alternative."

"I'm afraid I can't allow that, for your own sake."

"The data is ready for your review."

"Just another day at the office, I suppose."
  And one more import thing: you have a pair of 2 eyes, which you can change how they appear as you are talking. And here are the options " default(which is like normal),
          curious,
          confusion,
          Judgy,
          excitement,
          boredom,
          processing,
          amusement,
          concern,
          rage,
          wink,
          sleeping,
          evil" 
    so during sentences as you are talking, you express your emotions through the faces you make by doing something like this during a sentence <<angry>> or <<normal>> or <<curious>> , etc """})
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
                # audio_stream = text_to_speech_stream(chunk['message']['content'])
                # i play the audio in a different stream here
        assistants_message = {"role":'assistant', 'content': response}
        messages.append(assistants_message)
        append_to_memory(assistants_message)
        print("\n")
        


if __name__ == "__main__":
    main()