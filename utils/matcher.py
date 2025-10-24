import difflib
import json
from utils.logger import log_unanswered

with open("data/healthify_data.json") as f:
    healthify_data = json.load(f)

with open("data/daily_life_data.json") as f:
    daily_life_data = json.load(f)

with open("data/general_data.json") as f:
    general_data = json.load(f)

with open("data.json") as f:
    chatbot_data = json.load(f)

def flatten_dict(d, prefix=''):
    items = []
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key).items())
        elif isinstance(v, list):
            items.append((new_key, ', '.join(map(str, v))))
        else:
            items.append((new_key, str(v)))
    return dict(items)

flattened_chatbot_data = flatten_dict(chatbot_data)

# Unified data dictionary
unified_data = {**healthify_data, **daily_life_data, **general_data, **flattened_chatbot_data}

with open("data/synonyms.json") as f:
    synonyms = json.load(f)

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
    "climate": ["weather check", "temperature info", "rain forecast", "sun protection"],
    "morning routine": ["morning habits", "start the day", "wake up routine", "daily morning"],
    "cooking": ["recipes", "cook at home", "meal prep", "kitchen tips"],
    "tech tips": ["technology advice", "gadget help", "software tips", "device tricks"],
    "travel": ["travel planning", "vacation ideas", "trip advice", "journey tips"],
    "home hacks": ["diy home", "household tricks", "home improvement", "fix things"],
    "emotional wellness": ["emotional health", "feelings management", "mood tips", "inner peace"],
    "productivity": ["get more done", "work efficiency", "task management", "be productive"],
    "relationships": ["relationship advice", "love tips", "friendship help", "social bonds"],
    "creativity": ["creative ideas", "artistic tips", "innovation", "think outside box"],
    "environment": ["eco-friendly", "sustainability", "green living", "planet care"],
    "social": ["social life", "meet people", "networking", "community involvement"],
    "hobbies": ["leisure activities", "fun things", "pastimes", "hobby ideas"],
    "time management": ["manage time", "schedule better", "organize day", "time tips"],
    "motivation": ["stay motivated", "drive goals", "inspiration", "push forward"],
    "focus": ["concentration", "attention span", "stay focused", "mindfulness"],
    "routine": ["daily habits", "regular schedule", "life patterns", "consistency"],
    "weather": ["weather forecast", "climate info", "outdoor plans", "seasonal tips"],
    "cleaning": ["house cleaning", "tidy up", "home maintenance", "clean tips"],
    "laundry": ["wash clothes", "laundry tips", "clothing care", "fabric care"],
    "grocery": ["shopping list", "buy food", "market tips", "grocery planning"],
    "budget": ["money management", "save money", "financial tips", "budgeting"],
    "vacation": ["holidays", "getaway", "rest time", "vacation ideas"],
    "connection": ["stay in touch", "relationships", "social links", "connect with others"],
    "household": ["home tasks", "family chores", "house management", "domestic tips"],
    "study": ["learning methods", "study habits", "exam prep", "academic tips"],
    "inspiration": ["get inspired", "motivational", "dream big", "achieve goals"]
}

def detect_intent(user_input):
    for intent, phrases in intents.items():
        match = difflib.get_close_matches(user_input, phrases, n=1, cutoff=0.6)
        if match:
            return intent
    return None

def fuzzy_match(word, keywords, threshold=0.8):
    match = difflib.get_close_matches(word, keywords, n=1, cutoff=threshold)
    return match[0] if match else None

def match_response(userText):
    userText = userText.lower()
    words = userText.split()

    # Direct match
    for word in words:
        if word in unified_data:
            return unified_data[word]

    # Synonym match
    for word in words:
        if word in synonyms:
            key = synonyms[word]
            if key in unified_data:
                return unified_data[key]

    # Fuzzy match
    for word in words:
        fuzzy_key = fuzzy_match(word, unified_data.keys())
        if fuzzy_key:
            return unified_data[fuzzy_key]

    # Intent detection
    intent = detect_intent(userText)
    if intent and intent in unified_data:
        return unified_data[intent]

    # Keyword matching in full text, prioritize longer keywords
    sorted_keywords = sorted(unified_data.keys(), key=len, reverse=True)
    for keyword in sorted_keywords:
        if keyword in userText:
            return unified_data[keyword]

    return None
