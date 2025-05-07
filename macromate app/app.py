from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

HEADERS = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json"
}

API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

@app.route("/", methods=["GET", "POST"])
def index():
    foods = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    if request.method == "POST":
        query = request.form["query"]
        items = [item.strip() for item in query.split(",") if item.strip()]
        for item in items:
            res = requests.post(API_URL, headers=HEADERS, json={"query": item})
            if res.status_code == 200:
                data = res.json()
                for food in data.get("foods", []):
                    cals = food["nf_calories"]
                    protein = food["nf_protein"]
                    carbs = food["nf_total_carbohydrate"]
                    fat = food["nf_total_fat"]

                    foods.append({
                        "name": food["food_name"].title(),
                        "quantity": f'{food["serving_qty"]} {food["serving_unit"]} ({int(food["serving_weight_grams"])}g)',
                        "calories": round(cals),
                        "protein": round(protein),
                        "carbs": round(carbs),
                        "fat": round(fat),
                    })

                    total_calories += cals
                    total_protein += protein
                    total_carbs += carbs
                    total_fat += fat
            else:
                print(f"API error for item '{item}':", res.text)

    return render_template(
        "index.html",
        foods=foods,
        total_calories=round(total_calories),
        total_protein=round(total_protein),
        total_carbs=round(total_carbs),
        total_fat=round(total_fat),
    )

if __name__ == "__main__":
    app.run(debug=True)
