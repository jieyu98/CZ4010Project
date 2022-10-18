# API stuff
from flask import Flask, jsonify
from threading import Thread
from flask_restful import Resource, Api
from flask_cors import CORS

# Weather stuff
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests as req
import numpy as np
import random

app = Flask('')
api = Api(app)
CORS(app)

#################### Weather ####################
def csprng_weather():
  URL = 'http://www.weather.gov.sg/weather-rain-area-50km/'
  res = req.get(url=URL)
  if res.status_code == 200:
    print("Initiated")
    soup = BeautifulSoup(res.text, 'html.parser')
    rain_image_url = soup.find("img", alt="Rain areas over Singapore")
    rain_image_url = rain_image_url.get("src")

    response = req.get(rain_image_url)
    img = Image.open(BytesIO(response.content))
  else:
    print(f'Something went wrong for {URL} with status code : {res.status_code}.')

  g = bytearray(img.tobytes())

  cloud_arr = []

  for i in range(len(g)):
    if g[i] != 0:  # Remove white space
      pos = int(bin(i)[2:])  # Convert position of the cloud into binary
      cloud_arr.append(pos)  # Append to the array

  np.random.shuffle(cloud_arr)  # Shuffle array

  # Concatenate all the bits in the array into a string
  cloud_str = ""
  for i in cloud_arr:
    cloud_str += str(i)
  
  # Generate a psuedo random 2048 bits number
  p_random = ""
  for i in range(2048):
    j = random.randrange(0, 2)
    p_random += str(j)
  
  start = random.randrange(0, len(cloud_str))  # Determine start of sliding window
  end = start + 2048
  
  if end > len(cloud_str)-1:  # If sliding window exceeds pool of bits
    temp = cloud_str[(start-2048):start]
    cloud_str_subset = temp[::-1]
  else:
    cloud_str_subset = cloud_str[start:end]
  
  # XOR cloud string subset with psuedo random 2048 bits number
  res = [str(int(cloud_str_subset[i])^int(p_random[i])) for i in range(len(cloud_str_subset))]
  res = ''.join(res)

  print("Completed")
  return res

#################### API ####################
class csprng(Resource):
  def get(self):
    return csprng_weather()

# Creating API endpoint
api.add_resource(csprng, '/api/weather')

def run():
  app.run(host='0.0.0.0',port=7210)

t = Thread(target=run)
t.start()