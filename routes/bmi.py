from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()
session_store = {}

@router.post("/bmi")
async def bmi_flow(request: Request):
    body = await request.json()
    user_id = body.get("user_id")
    message = body.get("message").lower()

    if user_id not in session_store:
        session_store[user_id] = {"step": "height"}
        return JSONResponse(content={"reply": "Please enter your height in centimeters."})

    session = session_store[user_id]

    if session["step"] == "height":
        try:
            height_cm = float(message)
            session["height_cm"] = height_cm
            session["step"] = "weight"
            return JSONResponse(content={"reply": "Got it! Now enter your weight in kilograms."})
        except:
            return JSONResponse(content={"reply": "Please enter a valid number for height."})

    if session["step"] == "weight":
        try:
            weight_kg = float(message)
            height_m = session["height_cm"] / 100
            bmi = round(weight_kg / (height_m ** 2), 2)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 24.9:
                category = "Normal weight"
            elif bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"

            del session_store[user_id]
            return JSONResponse(content={"reply": f"Your BMI is {bmi}, which is considered {category}."})
        except:
            return JSONResponse(content={"reply": "Please enter a valid number for weight."})