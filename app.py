from flask import Flask, render_template, request
from nltk.chat.util import Chat, reflections

import difflib


app = Flask(__name__)

# Consolidated Chatbot Data
chatbot_data = {
    "who is ria": "Ria is Healthify’s personal AI coach. She provides daily health insights, personalized diet plans, and proactive suggestions to help you stay on track.",
    "who is your developer": "I’m Shivam Maurya’s creation, but I’m learning from you too.",
    "what does ria do": "Ria helps you improve your health by offering personalized diet plans, fitness tips, and smart tracking through tools like HealthifySnap.",
    "how does ria help with diet": "Ria analyzes your eating habits and recommends personalized diet plans based on your goals and preferences.",
    "how does ria help with fitness": "Ria suggests workouts tailored to your fitness level and tracks your activity to keep you motivated.",
    "how does ria track my meals": "Ria uses HealthifySnap to log meals from photos and estimate calories automatically.",
    "can ria help with weight loss": "Yes, Ria supports weight loss by guiding your diet, workouts, and daily habits. Users report losing up to 1.2 kg per week.",
    "is ria available 24/7": "Yes, Ria is always available through the Healthify app to answer questions and provide guidance.",
    "how does ria personalize advice": "Ria learns from your health data, preferences, and behavior to offer tailored recommendations.",
    "can ria remind me to drink water": "Yes, Ria can send hydration reminders and track your water intake.",
    "can ria track my steps": "Ria syncs with your device to monitor steps and encourages daily movement goals.",
    "does ria support mental health": "Ria offers tips for stress management, sleep hygiene, and emotional wellness.",
    "how do i talk to ria": "You can chat with Ria directly in the Healthify app. Just open the chatbot and start typing.",
    "can ria help with sleep": "Ria provides sleep tips and helps you build a consistent bedtime routine.",
    "does ria support chronic conditions": "Yes, Ria helps manage lifestyle diseases like diabetes and hypertension with diet and activity tracking.",
    "can ria track calories": "Ria automatically tracks calories using HealthifySnap and manual logging options.",
    "can ria help with motivation": "Ria sends encouraging messages, tracks progress, and celebrates your milestones to keep you motivated.",
    "can ria help with stress": "Ria offers breathing exercises, mindfulness tips, and reminders to take breaks.",
    "how does ria learn": "Ria uses AI to learn from your interactions, health data, and feedback to improve her suggestions over time.",
    "can ria help with grocery planning": "Ria can suggest grocery lists based on your diet plan and health goals.",
    "can ria help with cooking": "Ria recommends simple, healthy recipes based on your preferences and available ingredients.",
    "what is healthify": "Healthify is a modular healthcare platform with AI-powered tools like symptom checkers, clinic locators, and health calculators.",
    "how does healthifysnap work": "HealthifySnap lets you track food by simply clicking a photo before you eat. It uses AI to estimate calories and log meals.",
    "what is a personalized diet plan": "Healthify offers personalized diet plans tailored to your goals, lifestyle, and preferences.",
    "how do i track calories": "Healthify auto-tracks your calories using AI and image recognition. You can also log meals manually.",
    "how does healthify help with weight loss": "Healthify users report an average weight loss of 1.2 kg per week with personalized plans and coaching.",
    "what are lifestyle diseases": "Healthify helps manage lifestyle diseases like diabetes, hypertension, and obesity through diet, exercise, and AI guidance.",
    "how does healthify track steps": "Healthify syncs with your phone or wearable to track steps and encourages daily movement goals.",
    "how many messages has healthify exchanged": "Over 170 million messages have been exchanged between users and Healthify’s AI coach.",
    "what nutrition guidance does healthify offer": "Healthify provides AI-powered nutrition guidance based on your goals, health data, and preferences.",
    "what fitness plans are available": "Healthify offers gym and home workout plans tailored to your fitness level and goals.",
    "what are healthify’s smart features": "Smart features include Ria, HealthifySnap, proactive insights, auto-tracking, and personalized coaching.",
    "what is the subscription cost": "Healthify plans start at ₹999/month and include full access to AI coaching and smart tools.",
    "where can i download the healthify app": "You can download the Healthify app from the Play Store or App Store to get started.",
    "healthify": "Healthify is a modular healthcare platform with AI-powered tools like symptom checkers, clinic locators, and health calculators.",
    "appointment": "You can book an appointment by visiting the 'Clinics' section and selecting your preferred doctor and time slot.",
    "bmi": "BMI (Body Mass Index) is a measure of body fat based on height and weight. Healthify includes a BMI calculator in the Tools section.",
    "support": "You can contact Healthify support via the chatbot or email us at support@healthify.ai.",
    "symptom": "Our symptom checker lets you input symptoms and get AI-generated suggestions for possible conditions.",
    "clinic": "Use the 'Clinics' section to find nearby healthcare centers based on your location.",
    "tools": "Healthify offers tools like BMI calculator, calorie tracker, and appointment scheduler.",
    "emergency": "In case of emergency, please call your local emergency number or visit the nearest hospital. Healthify is not a substitute for urgent care.",
    "insurance": "Healthify does not currently process insurance claims, but you can find clinics that accept insurance in the 'Clinics' section.",
    "medication": "You can set up medication reminders using our health tools dashboard.",
    "mental": "Healthify includes resources for mental wellness and crisis support. You can chat with our AI or visit the 'Support' section.",
    "diet": "Visit the 'Health Tools' section for personalized diet tips based on your BMI and goals.",
    "vaccination": "You can check vaccination schedules and availability in the 'Clinics' section or ask our chatbot for guidance.",
    "covid": "Healthify provides up-to-date COVID-19 guidelines, symptoms, and vaccination info in the 'Updates' section.",
    "doctor": "Doctor availability is listed in the 'Clinics' section. You can filter by specialty and time slot.",
    "exercise": "Healthify recommends daily movement and offers exercise tips based on your health goals.",
    "sleep": "Good sleep is essential for health. Healthify offers sleep hygiene tips and tracking tools.",
    "hydration": "Staying hydrated is key. Our health dashboard includes reminders and hydration tracking.",
    "calories": "Use the calorie tracker in Healthify’s Tools section to monitor your intake and set goals.",
    "pregnancy": "Healthify offers pregnancy tracking, prenatal tips, and clinic recommendations.",
    "children": "You can find pediatric clinics and child health resources in the 'Clinics' and 'Support' sections.",
    "elderly": "Healthify includes resources for elder care, including mobility support and chronic condition management.",
    "diabetes": "Our health tools include blood sugar tracking and diet tips for managing diabetes.",
    "heart": "Healthify offers heart health tips, symptom checkers, and clinic filters for cardiologists.",
    "what is bmi": "BMI (Body Mass Index) is a measure of body fat based on height and weight. Healthify includes a BMI calculator in the Tools section.",
    "how to book an appointment": "You can book an appointment by visiting the 'Clinics' section and selecting your preferred doctor and time slot.",
    "how to contact support": "You can contact Healthify support via the chatbot or email us at support@healthify.ai.",
    "what is a symptom checker": "Our symptom checker lets you input symptoms and get AI-generated suggestions for possible conditions.",
    "where is the nearest clinic": "Use the 'Clinics' section to find nearby healthcare centers based on your location.",
    "what health tools are available": "Healthify offers tools like BMI calculator, calorie tracker, and appointment scheduler.",
    "what to do in an emergency": "In case of emergency, please call your local emergency number or visit the nearest hospital. Healthify is not a substitute for urgent care.",
    "does healthify support insurance": "Healthify does not currently process insurance claims, but you can find clinics that accept insurance in the 'Clinics' section.",
    "how to set medication reminders": "You can set up medication reminders using our health tools dashboard.",
    "what mental health resources are available": "Healthify includes resources for mental wellness and crisis support. You can chat with our AI or visit the 'Support' section.",
    "what are some diet tips": "Visit the 'Health Tools' section for personalized diet tips based on your BMI and goals.",
    "how to check vaccination info": "You can check vaccination schedules and availability in the 'Clinics' section or ask our chatbot for guidance.",
    "what are covid-19 guidelines": "Healthify provides up-to-date COVID-19 guidelines, symptoms, and vaccination info in the 'Updates' section.",
    "how to find available doctors": "Doctor availability is listed in the 'Clinics' section. You can filter by specialty and time slot.",
    "what’s a healthy breakfast": "A healthy breakfast could include oats, fruits, eggs, or yogurt. Try to include protein and fiber.",
    "how to stay hydrated": "Drink at least 2–3 liters of water daily. Carry a bottle and sip regularly.",
    "how much sleep do i need": "Adults need 7–9 hours of sleep. Avoid screens before bed and keep a consistent sleep schedule.",
    "how to reduce stress": "Try deep breathing, meditation, or short walks to reduce stress.",
    "what are good study tips": "Use the Pomodoro technique, take breaks, and avoid multitasking.",
    "how to be more productive": "Start your day with a to-do list, prioritize tasks, and avoid distractions.",
    "what’s a simple meal to cook": "Simple meals like stir-fry, sandwiches, or one-pot rice dishes are great for beginners.",
    "how to manage time better": "Use planners, set reminders, and break tasks into small chunks.",
    "how to stay motivated": "Set small goals, celebrate progress, and surround yourself with positive energy.",
    "how to improve focus": "Eliminate distractions, use noise-canceling headphones, and take short breaks to reset.",
    "what is self-care": "Take time for hobbies, rest, and reflection. Healthify supports mental wellness too.",
    "how to build a daily routine": "A good routine includes sleep, meals, movement, and time for learning or relaxation.",
    "what’s the weather like": "Check your local weather app or site for accurate updates. Dress accordingly!",
    "how to clean my room": "Clean one room at a time. Use music or timers to stay motivated.",
    "how to do laundry": "Sort clothes by color, use mild detergent, and air dry when possible.",
    "what to buy for groceries": "Make a list before shopping. Include fruits, veggies, grains, and proteins.",
    "how to manage my budget": "Track expenses, avoid impulse buys, and save a little each month.",
    "what to pack for travel": "Pack light, carry essentials, and check local guidelines before traveling.",
    "how to stay socially connected": "Stay connected with friends and family. Healthify encourages community support.",
    "breakfast": "A healthy breakfast could include oats, fruits, eggs, or yogurt. Try to include protein and fiber.",
    "exercise": "Regular exercise like walking, yoga, or cycling helps maintain physical and mental health.",
    "sleep": "Adults need 7–9 hours of sleep. Avoid screens before bed and keep a consistent sleep schedule.",
    "hydration": "Staying hydrated is key. Our health dashboard includes reminders and hydration tracking.",
    "stress": "Try deep breathing, meditation, or short walks to reduce stress.",
    "study tips": "Use the Pomodoro technique, take breaks, and avoid multitasking.",
    "productivity": "Start your day with a to-do list, prioritize tasks, and avoid distractions.",
    "cooking": "Simple meals like stir-fry, sandwiches, or one-pot rice dishes are great for beginners.",
    "time management": "Use planners, set reminders, and break tasks into small chunks.",
    "motivation": "Set small goals, celebrate progress, and surround yourself with positive energy.",
    "focus": "Eliminate distractions, use noise-canceling headphones, and take short breaks to reset.",
    "self care": "Take time for hobbies, rest, and reflection. Healthify supports mental wellness too.",
    "routine": "A good routine includes sleep, meals, movement, and time for learning or relaxation.",
    "weather": "Check your local weather app or site for accurate updates. Dress accordingly!",
    "cleaning": "Clean one room at a time. Use music or timers to stay motivated.",
    "laundry": "Sort clothes by color, use mild detergent, and air dry when possible.",
    "grocery": "Make a list before shopping. Include fruits, veggies, grains, and proteins.",
    "budget": "Track expenses, avoid impulse buys, and save a little each month.",
    "travel": "Pack light, carry essentials, and check local guidelines before traveling.",
    "social": "Stay connected with friends and family. Healthify encourages community support.",
    "can you match similar words like calory and calorie": "Yes, I can match similar words using fuzzy matching. For example, 'calory' matches 'diet'.",
    "do you log unanswered questions for updates": "Yes, I log unanswered questions to a file to improve my responses over time.",
    "can you show suggestions when you don’t know the answer": "When I don't know the answer, I log the question and provide a helpful response. You can try rephrasing or asking about health topics."
}

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


# all_data is now replaced by chatbot_data

synonyms = {
    "calory": "diet",
    "water": "hydration",
    "rest": "sleep",
    "doc": "ria",
    "coach": "ria",
    "fat": "bmi"
}

intents = {
    "bmi": ["calculate bmi", "check my bmi", "body mass index", "am I overweight"],
    "diet": ["healthy food", "meal plan", "what should I eat", "diet tips"],
    "sleep": ["how to sleep better", "sleep tips", "I feel tired", "rest advice"],
    "hydration": ["drink water", "how much water", "hydration tips"],
    "ria": ["who are you", "your name", "who made you", "developer info"]
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
        if word in chatbot_data:
            answer = chatbot_data[word]
            return ria_response(answer) if is_addressed_to_ria else answer

    # Check synonym match
    for word in words:
        if word in synonyms:
            key = synonyms[word]
            if key in chatbot_data:
                answer = chatbot_data[key]
                return ria_response(answer) if is_addressed_to_ria else answer

    # Check fuzzy match
    for word in words:
        fuzzy_key = fuzzy_match(word, chatbot_data.keys())
        if fuzzy_key:
            answer = chatbot_data[fuzzy_key]
            return ria_response(answer) if is_addressed_to_ria else answer

    # Detect intent
    intent = detect_intent(userText)
    if intent and intent in chatbot_data:
        answer = chatbot_data[intent]
        return ria_response(answer) if is_addressed_to_ria else answer

    # Keyword matching in full text
    for keyword, answer in chatbot_data.items():
        if keyword in userText:
            return ria_response(answer) if is_addressed_to_ria else answer

    # Log unanswered question
    log_unanswered(userText)

    return "I'm still learning and improving. I don't have an answer for that yet, but your question helps me grow smarter!"


if __name__ == "__main__":
    app.run(debug=True)

def log_feedback(question, feedback):
    with open("feedback.txt", "a") as file:
        file.write(f"{question} | {feedback}\n")
