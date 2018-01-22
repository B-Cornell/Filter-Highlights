import io
import os
import argparse
import requests

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


outputfile = open("Output.txt", "w")
#API_ENDPOINT = "https://vision.googleapis.com/v1/images"
#API_KEY = "AIzaSyBcmZNkmvDbR4i49ZQzxj6rYDnBK2m84N4"




def first_process():
# Instantiates a client
    client1 = vision.ImageAnnotatorClient()


# The name of the image file to annotate
    file_name = os.path.join(
    	os.path.dirname(__file__),
    	'/Users/sungminpark/Desktop/highlight.png')

# Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
    	content = image_file.read()

    image = types.Image(content=content)
    im = types.Image(content=content)
    # Performs label detection on the entire image
    response1 = client1.text_detection(image=image)
    text = response1.text_annotations
    return text


def second_process(iteration):
	# Instantiates a client
    client1 = vision.ImageAnnotatorClient()

# The name of the image file to annotate
    file_name = os.path.join(
    	os.path.dirname(__file__),
    	'/Users/sungminpark/Desktop/highlight.png')
# Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
    	content = image_file.read()

    image = types.Image(content=content)
    im = types.Image(content=content)
    # Performs label detection on the entire image
    response1 = client1.text_detection(image=image)
    text = response1.text_annotations

    number = 0
    for word in text:
    	if (number == iteration):
			bound = word.bounding_poly.vertices
        number += 1
	
    return bound



def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""
    #vects = second_process()
    client1 = vision.ImageAnnotatorClient()

    im = Image.open(image_file)
    i = 1
    print("Yellow:\n")
    outputfile.write("Yellow:\n\n")
    while(1):
    	vects = second_process(i)
    	
    	im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    	string = "output"+str(i)+".png"
    	im2.save(string, 'PNG')
    	file_name = os.path.join(
    	os.path.dirname(__file__),
    	'/Users/sungminpark/Desktop/'+ string)
    	with io.open(file_name, 'rb') as image_file:
    		content = image_file.read()
    	image = types.Image(content=content)
    	response = client1.image_properties(image=image)
    	props = response.image_properties_annotation
    	n = 0
    	for color in props.dominant_colors.colors:
    		if(n==0):
    			red=((color.color.red))
        		green=((color.color.green))
        		blue=((color.color.blue))
        		#print("red:", red)
        		#print("green:", green)
        		#print("blue:", blue)
        	n += 1


        if((red > 190 and green > 190) and (blue < 150)):
 			#print("Highlighted")   
 			with io.open(file_name, 'rb') as image_file:
 				content = image_file.read()
 			newimage = types.Image(content=content)
 			newim = types.Image(content=content)
 			response1 = client1.text_detection(image=newimage)
 			texts = response1.text_annotations

 			b = 0
 			
 			for text in texts:
 				if(b==0):
 					store = str(text.description)
 					outputfile.write(store)
 					print(store) 
 				b+=1
    	i += 1


   

parser = argparse.ArgumentParser()
parser.add_argument('image_file', help='The image you\'d like to crop.')
parser.add_argument('mode', help='Set to "crop" or "draw".')
args = parser.parse_args()

parser = argparse.ArgumentParser()

if args.mode == 'crop':
    crop_to_hint(args.image_file)


outputfile.close()

#print(third_process())



