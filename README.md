Author: Basil Vetas

Date: 10/9/17

Playing around with AngularJS, Tornado and Clarifai's API: https://clarifai.com/developer/

First install the client server globally with: 

	npm install http-server -g

To retrieve image URLs for training data and create hotdogs.txt file:

    curl https://www.flickr.com/search/?text=%22hot%20dog%22%20food | grep -o "img.src='[^']*'" | grep -o "'[^']*'" | sed "s/'//g" | perl -ne 'print "https:$_"' | sort -u > ./hotdogs.txt

To start Tornado Server:

	python3 hotdog.py

To start Angular Client:

	http-server

Example URL: http://www.freepngimg.com/download/hot_dog/9-2-hot-dog-png-picture.png