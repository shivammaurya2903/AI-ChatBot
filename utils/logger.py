def log_unanswered(question):
    with open("unanswered.txt", "a", encoding="utf-8") as file:
        file.write(question + "\n")

def log_feedback(question: str, feedback: str):
    with open("feedback.txt", "a", encoding="utf-8") as file:
        file.write(f"{question} | {feedback}\n")
