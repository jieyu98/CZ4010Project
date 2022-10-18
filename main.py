# API stuff
from flask import Flask, jsonify
from threading import Thread
from flask_restful import Resource, Api

# Weather stuff
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests as req
import numpy as np
import random

app = Flask('')
api = Api(app)

#################### Weather ####################
def csprng_weather():
  URL = 'http://www.weather.gov.sg/weather-rain-area-50km/'
  res = req.get(url=URL)
  if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    rain_image_url = soup.find("img", alt="Rain areas over Singapore")
    rain_image_url = rain_image_url.get("src")
    print(rain_image_url)

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
    print("Reverso Magico")
    temp = cloud_str[(start-2048):start]
    cloud_str_subset = temp[::-1]
  else:
    cloud_str_subset = cloud_str[start:end]
  
  # XOR cloud string subset with psuedo random 2048 bits number
  res = int(cloud_str_subset) ^ int(p_random)
  res = bin(res)[2:]

  count0 = 0
  count1 = 0
  for i in res:
    if i == "0":
      count0 += 1
    else:
      count1 += 1
  
  return res

#################### API ####################
class csprng(Resource):
  def get(self):
    # return "Hi"
    return csprng_weather()

# Creating API endpoint
api.add_resource(csprng, '/api/weather')

def run():
  app.run(host='0.0.0.0',port=7210)

t = Thread(target=run)
t.start()