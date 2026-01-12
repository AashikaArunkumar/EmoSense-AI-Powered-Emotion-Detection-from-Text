from flask import Flask, request, jsonify, render_template
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)
model = pickle.load(open("emotion_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    cleaned = preprocess_text(text)
    vector = tfidf.transform([cleaned])
    prediction = model.predict(vector)[0]
    emotion = label_encoder.inverse_transform([prediction])[0]

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)
