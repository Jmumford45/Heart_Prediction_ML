from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource, fields
import joblib
from pickle import load
from model import pipelineTransform, reorder

flask_app = Flask(__name__, static_folder="UI/frontend/build")
app = Api(app = flask_app,
                version="1.0",
                title="Predict Heart Diseased",
                description = "Predicts probability of heart disease")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model("Prediction params",
                                {"Age": fields.Integer(required = True, decription = "Age number", help="Field cannot be blank"),
                                 "Sex": fields.String(required=True, description="Sex", help="field cannot be blank"),
                                 "ChestPain": fields.String(required=True, description="Type of Chest Pain if any", help="Field cannot be blank"),
                                 "RestingBP": fields.Float(required=True, description="Blood Pressure at rest", help="field cannot be blank"),
                                 "Cholesterol": fields.Integer(required=True, description='Level of cholesterol', help='field cannot be blank'),
                                 "FastingBS": fields.Float(required=True, description="Yes or No", help="field cannot be blank"),
                                 "RestingECG": fields.String(required=True, description="Heart beats rythme", help="field cannot be blank"),
                                 "MaxHR": fields.Float(required=True, description="Maximum Heart Rate", help="field cannot be blank"),
                                 "ExerciseAngina": fields.String(required=True, description="Diagnosed condition", help="Field cannot be blank"),
                                 "OldPeak": fields.Float(required=True, description="Measured heart performance previously", help="field cannot be blank"),
                                 "ST_Slope": fields.String(required=True, description = "Level of elevation of heart beats", help="field cannot be blank")})

classifier = joblib.load('classifer.joblib')
scaler = joblib.load('scaler.joblib')

with open('headers.pkl', 'rb') as f:
    headers_df = load(f)

@app.route("/prediction")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)
	def post(self):
		try: 
			formData = request.json
			#print(type(formData))
			#print(formData)
			df_json = pipelineTransform(formData, headers_df)
			#print(df_json)
			df_predict = reorder(df_json, headers_df)
			#data = [val for val in formData.values()]
			predictVal = classifier.predict_proba(df_predict)
			#print(predictVal)
			#print("result: Probability of Heart Disease: ", predictVal[0])
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Probability of Heart Disease: " + str(predictVal)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})

app.add_resource(MainClass, '/prediction')



