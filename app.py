from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load Model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Numeric Inputs
    area = float(request.form["area"])
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    parking = int(request.form["parking"])
    age = int(request.form["age"])
    floor = int(request.form["floor"])
    total_floors = int(request.form["total_floors"])
    balcony = int(request.form["balcony"])

    school_distance = float(request.form["school_distance"])
    hospital_distance = float(request.form["hospital_distance"])
    metro_distance = float(request.form["metro_distance"])
    market_distance = float(request.form["market_distance"])

    # Dropdown Inputs
    location = request.form["location"]
    furnishing = request.form["furnishing"]
    lift = request.form["lift"]
    gym = request.form["gym"]
    pool = request.form["pool"]

    # Input Data
    data = {
        "Area": [area],
        "Bedrooms": [bedrooms],
        "Bathrooms": [bathrooms],
        "Parking": [parking],
        "Age": [age],
        "Floor": [floor],
        "Total_Floors": [total_floors],
        "Balcony": [balcony],
        "School_Distance": [school_distance],
        "Hospital_Distance": [hospital_distance],
        "Metro_Distance": [metro_distance],
        "Market_Distance": [market_distance],

        "Location_Kolkata": [0],
        "Location_Mumbai": [0],
        "Location_Patna": [0],

        "Furnishing_Semi-Furnished": [0],
        "Furnishing_Unfurnished": [0],

        "Lift_Yes": [0],
        "Gym_Yes": [0],
        "Swimming_Pool_Yes": [0]
    }

    # Location Encoding
    if location == "Kolkata":
        data["Location_Kolkata"] = [1]
    elif location == "Mumbai":
        data["Location_Mumbai"] = [1]
    elif location == "Patna":
        data["Location_Patna"] = [1]

    # Furnishing Encoding
    if furnishing == "Semi-Furnished":
        data["Furnishing_Semi-Furnished"] = [1]
    elif furnishing == "Unfurnished":
        data["Furnishing_Unfurnished"] = [1]

    # Amenities
    if lift == "Yes":
        data["Lift_Yes"] = [1]

    if gym == "Yes":
        data["Gym_Yes"] = [1]

    if pool == "Yes":
        data["Swimming_Pool_Yes"] = [1]

    # DataFrame
    input_df = pd.DataFrame(data)

    # Prediction
    prediction = model.predict(input_df)[0]

    # Dynamic House Image
    if prediction < 1200000:
        image = "small_house.jpg"
    elif prediction < 2900000:
        image = "medium_house.jpg"
    else:
        image = "luxury_house.jpg"

    return render_template(
        "result.html",
        prediction=f"₹ {prediction:,.0f}",
        image=image
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)