from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('model/house_price_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    area = float(request.form['area'])
    bhk = int(request.form['bhk'])
    bathroom = int(request.form['bathroom'])
    locality = request.form['locality']

    prediction = "Prediction Coming Soon"

    return render_template(
        'index.html',
        prediction_text=prediction
    )


if __name__ == "__main__":
    app.run(debug=True)