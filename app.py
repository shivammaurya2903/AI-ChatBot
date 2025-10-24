from flask import Flask, render_template, request
from nltk.chat.util import Chat, reflections
from utils.matcher import unified_data, synonyms, intents

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

synonyms = {
    "calory": "diet",
    "calories": "diet",
    "food": "diet",
    "meal": "diet",
    "nutrition": "diet",
    "water": "hydration",
    "drink": "hydration",
    "fluid": "hydration",
    "rest": "sleep",
    "nap": "sleep",
    "bedtime": "sleep",
    "tired": "sleep",
    "doc": "ria",
    "coach": "ria",
    "assistant": "ria",
    "ai": "ria",
    "fat": "bmi",
    "weight": "bmi",
    "overweight": "bmi",
    "obese": "bmi",
    "exercise": "fitness",
    "workout": "fitness",
    "gym": "fitness",
    "run": "fitness",
    "walk": "fitness",
    "stress": "mental",
    "anxiety": "mental",
    "depression": "mental",
    "mood": "mental",
    "mind": "mental",
    "appointment": "clinic",
    "doctor": "clinic",
    "hospital": "clinic",
    "checkup": "clinic",
    "symptom": "health",
    "illness": "health",
    "disease": "health",
    "pain": "health",
    "sick": "health",
    "emergency": "urgent",
    "crisis": "urgent",
    "help": "urgent",
    "911": "urgent",
    "vaccination": "vaccine",
    "shot": "vaccine",
    "immunization": "vaccine",
    "covid": "pandemic",
    "coronavirus": "pandemic",
    "virus": "pandemic",
    "pregnancy": "maternity",
    "baby": "maternity",
    "child": "maternity",
    "elderly": "senior",
    "old": "senior",
    "aging": "senior",
    "diabetes": "chronic",
    "hypertension": "chronic",
    "heart": "chronic",
    "condition": "chronic",
    "medication": "reminder",
    "pill": "reminder",
    "drug": "reminder",
    "remind": "reminder",
    "mental": "wellness",
    "selfcare": "wellness",
    "routine": "wellness",
    "habit": "wellness",
    "budget": "finance",
    "money": "finance",
    "expense": "finance",
    "save": "finance",
    "travel": "trip",
    "vacation": "trip",
    "journey": "trip",
    "flight": "trip",
    "social": "connection",
    "friend": "connection",
    "family": "connection",
    "community": "connection",
    "cleaning": "household",
    "laundry": "household",
    "grocery": "household",
    "cook": "household",
    "study": "learning",
    "focus": "learning",
    "productivity": "learning",
    "time": "learning",
    "motivation": "inspiration",
    "goal": "inspiration",
    "success": "inspiration",
    "achievement": "inspiration",
    "weather": "climate",
    "temperature": "climate",
    "rain": "climate",
    "sun": "climate"
}

intents = {
    "bmi": ["calculate bmi", "check my bmi", "body mass index", "am I overweight", "what is my bmi", "bmi calculator"],
    "diet": ["healthy food", "meal plan", "what should I eat", "diet tips", "nutrition advice", "healthy eating"],
    "sleep": ["how to sleep better", "sleep tips", "I feel tired", "rest advice", "insomnia", "sleep hygiene"],
    "hydration": ["drink water", "how much water", "hydration tips", "stay hydrated", "water intake"],
    "ria": ["who are you", "your name", "who made you", "developer info", "what is ria", "about ria"],
    "fitness": ["exercise tips", "workout plan", "how to get fit", "physical activity", "gym routine"],
    "mental": ["stress relief", "anxiety help", "mental health tips", "mood improvement", "emotional support"],
    "clinic": ["book appointment", "find doctor", "nearby hospital", "medical checkup", "health clinic"],
    "health": ["symptom checker", "general health", "wellness tips", "preventive care", "health advice"],
    "urgent": ["emergency help", "what to do in crisis", "immediate assistance", "urgent care"],
    "vaccine": ["vaccination info", "get vaccinated", "immunization schedule", "vaccine availability"],
    "pandemic": ["covid guidelines", "coronavirus info", "pandemic updates", "virus prevention"],
    "maternity": ["pregnancy tips", "baby care", "child health", "prenatal advice"],
    "senior": ["elderly care", "aging tips", "senior health", "mobility support"],
    "chronic": ["diabetes management", "hypertension tips", "heart health", "chronic conditions"],
    "reminder": ["medication reminder", "set alarm", "pill schedule", "remind me"],
    "wellness": ["self-care tips", "daily routine", "mental wellness", "lifestyle habits"],
    "finance": ["budget tips", "save money", "financial planning", "expense tracking"],
    "trip": ["travel tips", "vacation planning", "packing advice", "trip preparation"],
    "connection": ["social tips", "stay connected", "friendship advice", "community support"],
    "household": ["cleaning tips", "laundry advice", "grocery planning", "home organization"],
    "learning": ["study tips", "improve focus", "productivity hacks", "time management"],
    "inspiration": ["motivation tips", "set goals", "achieve success", "stay inspired"],
    "climate": ["weather check", "temperature info", "rain forecast", "sun protection"]
}



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

    # Check direct match
    for word in words:
        if word in unified_data:
            answer = unified_data[word]
            return ria_response(answer) if is_addressed_to_ria else answer

    # Check synonym match
    for word in words:
        if word in synonyms:
            key = synonyms[word]
            if key in unified_data:
                answer = unified_data[key]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Check fuzzy match
    for word in words:
        fuzzy_key = fuzzy_match(word, unified_data.keys())
        if fuzzy_key:
            answer = unified_data[fuzzy_key]
            return ria_response(answer) if is_addressed_to_ria else answer

    # Detect intent
    intent = detect_intent(userText)
    if intent and intent in unified_data:
        answer = unified_data[intent]
        return ria_response(answer) if is_addressed_to_ria else answer

    # Keyword matching in full text
    for keyword, answer in unified_data.items():
        if keyword in userText:
            return ria_response(answer) if is_addressed_to_ria else answer

    # Log unanswered question
    log_unanswered(userText)

    # Try web search fallback
    web_answer = web_search_fallback(userText)
    if web_answer:
        return ria_response(web_answer) if is_addressed_to_ria else web_answer

    suggestions = [
        "Try asking about health tips, diet plans, or fitness advice.",
        "You can ask questions like 'What is BMI?' or 'How to stay hydrated?'.",
        "For general knowledge, try topics like science, history, or geography.",
        "If it's about Healthify, ask about Ria, appointments, or tools."
    ]
    import random
    suggestion = random.choice(suggestions)
    return f"I'm still learning and improving. I don't have an answer for that yet, but your question helps me grow smarter! {suggestion}"


if __name__ == "__main__":
    app.run(debug=True)

def log_feedback(question, feedback):
    with open("feedback.txt", "a") as file:
        file.write(f"{question} | {feedback}\n")
