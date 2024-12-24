from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load Dataset
df = pd.read_csv('megaGymDataset.csv')
df['Desc'] = df['Desc'].fillna('')
df['features'] = (df['Title'].fillna('') + ' ' + df['Desc'] + ' ' + df['Type'].fillna('') + ' ' +
                  df['BodyPart'].fillna('') + ' ' + df['Equipment'].fillna('') + ' ' + df['Level'].fillna(''))

# TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['features'])


def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "Underweight"
        advice = "Consider a nutrient-rich diet to gain weight healthily."
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        advice = "Maintain your balanced diet and regular exercise."
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        advice = "Focus on a calorie-deficit diet and regular workouts."
    else:
        category = "Obesity"
        advice = "Consult a nutritionist and incorporate daily exercise."
    return round(bmi, 2), category, advice


def recommend_exercises(goal, body_type, fitness_level, equipment, body_part, top_n=5):
    user_preferences = f"{goal} {body_type} {fitness_level} {equipment} {body_part}"
    user_vector = tfidf_vectorizer.transform([user_preferences])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    recommendations = df.iloc[top_indices][['Title', 'Type', 'BodyPart', 'Equipment', 'Level', 'Desc']]
    return recommendations.to_dict(orient='records')


@app.route('/')
def index():
    options = {
        "goals": ["Muscle Gain", "Weight Loss", "Endurance", "Flexibility", "Strength", "Toning"],
        "body_types": ["Ectomorph", "Mesomorph", "Endomorph"],
        "fitness_levels": ["Beginner", "Intermediate", "Advanced"],
        "equipment": ["Dumbbells", "Barbell", "Kettlebell", "Resistance Bands", "Bodyweight"],
        "body_parts": [
            "Chest", "Back", "Arms", "Legs", "Core", "Shoulders", "Full Body", "Glutes", "Biceps", "Triceps"
        ]
    }
    return render_template('index.html', options=options)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    weight = float(data['weight'])
    height = float(data['height'])
    bmi, category, bmi_advice = calculate_bmi(weight, height)

    workouts = recommend_exercises(
        data['goal'], data['body_type'], data['fitness_level'],
        data['equipment'], data['body_part']
    )

    return jsonify({
        'bmi': bmi,
        'category': category,
        'bmi_advice': bmi_advice,
        'diet': 'Include a variety of nutrient-rich foods for optimal results.',
        'workouts': workouts
    })


if __name__ == '__main__':
    app.run(debug=True)
