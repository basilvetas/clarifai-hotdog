from clarifai import rest
from clarifai.rest import ClarifaiApp
from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

## API to handle post requests for hot dog image prediction
class ModelHandler(RequestHandler):	
	def initialize(self, app):
		self.app = app		

	def set_default_headers(self):
		super(ModelHandler, self).set_default_headers()
		self.set_header('Access-Control-Allow-Origin', 'http://localhost:8080')
		self.set_header('Access-Control-Allow-Credentials', 'true')	

	def post(self):
		self.set_header("Content-Type", "text/plain")
		url = self.get_body_argument('url')    				
		prediction = predictImage(self.app, url)
		label = lambda p: "Hotdog!" if p > .5 else "Not hotdog!"		
		p = prediction['outputs'][0]['data']['concepts'][0]['value']
		print("Prediction: ", label(p), str(round(p*100, 2)) + "%")
		self.write(prediction)

# Deletes old image inputs and models from the app object so we can re-train without conflict
def clearApp(app):
	app.inputs.delete_all()
	app.models.delete_all()
	return app

# Uses images from hotdogs.txt to train the model, returns the app object with trained model
def trainModel(app):	 
	print("Training Model...") # train model
	file = open("hotdogs.txt")
	lines = file.readlines()		

	for i, line in enumerate(lines):
		url = line.strip()
		app.inputs.create_image_from_url(url, image_id="id" + str(i), concepts=["hot dog"])		
	
	model = app.models.create("hotdogs", concepts=["hot dog"])		
	model = model.train()
	return app

# Predicts whether the image url param contains a hot dog, returns dict of results
def predictImage(app, url):
	print("Predicting Image...")
	model = app.models.get("hotdogs")		
	pred = model.predict_by_url(url=url)	
	return pred

# Trains the Clarifai app model, passes app object into request handler
def make_app():	
	app = ClarifaiApp(api_key=open("key.txt").read())
	app = clearApp(app)
	app = trainModel(app)		
	print("Model Trained Successfully")
	return Application([
		(r"/predict/", ModelHandler, dict(app = app)),
	])

if __name__ == '__main__':	
	app = make_app()
	app.listen(7777)
	IOLoop.current().start()
