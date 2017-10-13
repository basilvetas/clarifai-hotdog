Author: Basil Vetas

Date: 10/9/17

Playing around with AngularJS, Tornado Web Server and Clarifai's API. The app allows you to submit an image URL and it predicts what is in the image, either: Hotdog! or Not hotdog!

To run the server, you'll need to get an API Key from Clarifai by signing up at: https://clarifai.com/developer/.  Save this key in a file called key.txt

First install the client server globally with: 

	npm install http-server -g

To retrieve image URLs for training data and create hotdogs.txt file:

    curl https://www.flickr.com/search/?text=%22hot%20dog%22%20food | grep -o "img.src='[^']*'" | grep -o "'[^']*'" | sed "s/'//g" | perl -ne 'print "https:$_"' | sort -u > ./hotdogs.txt

The Tornado Web Server is located in the file hotdog.py. To start server on localhost:7777:

	python3 hotdog.py

(note sometimes the first time you run the server Clarifai API responds with an error -- if this happens just re-run it)

The AngularJS Client is located in the file index.html. To start client on localhost:8080:

	http-server

Example URL to submit: http://bit.ly/2xDnq7Z