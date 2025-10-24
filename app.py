from flask import Flask, render_template, request
from nltk.chat.util import Chat, reflections
from utils.matcher import unified_data, synonyms, intents, flattened_chatbot_data, general_data, daily_life_data, healthify_data

import difflib
import json
import requests

app = Flask(__name__)

pairs = [
    [r"hi|hello|hey |hii", ["Hello! How can I help you today?"]],
    [r"how are you?", ["I'm doing well, thank you!"]],
    [r"what is your name?", ["I'm Ria, your Healthify assistant."]],
    [r"who are you?", ["I'm Ria, your Healthify assistant, here to help with health and daily tips."]],
    [r"tell me about yourself", ["I'm Ria, an AI assistant for Healthify, providing health insights, diet plans, and more."]],
    [r"what can you do?", ["I can help with health tips, appointments, and daily questions."]],
    [r"what is the time?", ["I'm not wearing a watch, but your device can tell you!"]],
    [r"bye|goodbye", ["Goodbye! Stay healthy!"]],
]

chatbot = Chat(pairs, reflections)

# Data sources in priority order: generalchatbot, general, daily life, healthify
data_sources = [flattened_chatbot_data, general_data, daily_life_data, healthify_data]


def detect_intent(user_input):
    for intent, phrases in intents.items():
        match = difflib.get_close_matches(user_input, phrases, n=1, cutoff=0.6)
        if match:
            return intent
    return None

def ria_response(answer):
    return f"{answer}  Remember, you’re doing great—Ria’s here to support you every step of the way!"


def fuzzy_match(word, keywords, threshold=0.8):
    match = difflib.get_close_matches(word, keywords, n=1, cutoff=threshold)
    return match[0] if match else None


def log_unanswered(question):
    with open("unanswered.txt", "a", encoding="utf-8") as file:
        file.write(question + "\n")

def web_search_fallback(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url)
        data = response.json()
        if 'AbstractText' in data and data['AbstractText']:
            return data['AbstractText']
        elif 'Answer' in data and data['Answer']:
            return data['Answer']
        elif 'Definition' in data and data['Definition']:
            return data['Definition']
        else:
            return None
    except Exception as e:
        print(f"Error in web search: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg').lower()

    # First, try to get response from pairs using the Chat object
    response = chatbot.respond(userText)
    if response:
        return (response)

    words = userText.split()
    is_addressed_to_ria = "ria" in words

    # Check direct match with priority
    for word in words:
        for data in data_sources:
            if word in data:
                answer = data[word]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Check synonym match with priority
    for word in words:
        if word in synonyms:
            key = synonyms[word]
            for data in data_sources:
                if key in data:
                    answer = data[key]
                    return ria_response(answer) if is_addressed_to_ria else answer

    # Check fuzzy match with priority
    for word in words:
        for data in data_sources:
            fuzzy_key = fuzzy_match(word, data.keys())
            if fuzzy_key:
                answer = data[fuzzy_key]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Detect intent with priority
    intent = detect_intent(userText)
    if intent:
        for data in data_sources:
            if intent in data:
                answer = data[intent]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Keyword matching in full text with priority
    for data in data_sources:
        sorted_keywords = sorted(data.keys(), key=len, reverse=True)
        for keyword in sorted_keywords:
            if keyword in userText:
                answer = data[keyword]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Log unanswered question
    log_unanswered(userText)

    # Try web search fallback
    web_answer = web_search_fallback(userText)
    if web_answer:
        return ria_response(web_answer) if is_addressed_to_ria else web_answer

    suggestions = [
        "Try asking about health tips, diet plans, or fitness advice.",
        "For general knowledge, try topics like science, history, or geography.",
        "If it's about Healthify, ask about Ria, appointments, or tools."
    ]
    import random
    suggestion = random.choice(suggestions)
    return f"I'm still learning and improving. I don't have an answer for that yet, but your question helps me grow smarter! {suggestion}"


if __name__ == "__main__":
    app.run(debug=True)


