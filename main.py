# API stuff
from flask import Flask, request
from threading import Thread
from flask_restful import Resource, Api
from flask_cors import CORS

# Weather stuff
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests as req
import random
import math
from Crypto.Hash import keccak

app = Flask('')
api = Api(app)
print(api)
CORS(app)


#################### Weather ####################
def csprng_weather():
  URL = 'http://www.weather.gov.sg/weather-rain-area-50km/'
  res = req.get(url=URL)
  if res.status_code == 200:
    print("Weather initiated")
    soup = BeautifulSoup(res.text, 'html.parser')
    rain_image_url = soup.find("img", alt="Rain areas over Singapore")
    rain_image_url = rain_image_url.get("src")

    response = req.get(rain_image_url)
    img = Image.open(BytesIO(response.content))
  else:
    print(
      f'Something went wrong for {URL} with status code : {res.status_code}.')

  g = bytearray(img.tobytes())

  cloud_str_unpadded = ""
  cloud_str_padded = ""

  for i in range(len(g)):
    if g[i] != 0:  # Remove white space
      pos = str(int(bin(i)[2:]))  # Convert position of the cloud into binary
      pos_padded = pos.zfill(20)

      cloud_str_unpadded += pos
      cloud_str_padded += pos_padded

  return [cloud_str_unpadded, cloud_str_padded]


def unpad(cloud_str_padded):
  cloud_arr = []

  for i in range(int(len(cloud_str_padded) / 20)):
    cloud_arr.append(int((cloud_str_padded[i * 20:20 * (i + 1)])))

  return cloud_arr


def split_mouse(mouse_bits, cloud_arr):
  cloud_bits = math.ceil(math.log(len(cloud_arr), 2))
  shuffles = len(cloud_arr) - 1
  tot = cloud_bits * shuffles  # Total bits required to full shuffle
  hashes = math.ceil(tot / 512)  # Number of hashes required
  split_size = math.floor(
    len(mouse_bits) /
    hashes)  # Divide mouse_bits into equal portions as hash input

  return split_size, hashes


def fisher_yates(arr, shuffle_arr):
  print("Length of shuffle_arr: ", len(shuffle_arr))
  last_index = len(arr) - 1

  while last_index > 0 and len(shuffle_arr) > 0:
    rand_index = int(shuffle_arr.pop(0)) % last_index
    temp = arr[last_index]
    arr[last_index] = arr[rand_index]
    arr[rand_index] = temp
    last_index -= 1


def shuffle_bits(mouse_bits,
                 cloud_arr):  # To shuffle after html shows raw bits
  shuffle_str = ""
  shuffle_arr = []
  k = keccak.new(digest_bits=512)  # Keccak object

  # Retrieve the size of each split, and the number of splits required
  split_size, hashes = split_mouse(mouse_bits, cloud_arr)
  print("hashes is", hashes)
  print("split size is ", split_size)
  for i in range(hashes):

    # Retrieve portion of mouse_bits to input into hash
    cur_input = mouse_bits[i * split_size:split_size * (i + 1)]
    k = keccak.new(digest_bits=512)  # Keccak object
    k.update(
      str.encode(cur_input))  # Convert string to bytes and input to Keccak
    output = k.hexdigest()

    shuffle_str += str(hex_to_bin(output))

  cloud_bits = math.ceil(
    math.log(len(cloud_arr), 2)
  )  # TO find the max bits required to retrieve a position within cloud_arr
  for i in range(len(cloud_arr) - 1):
    cur_input = shuffle_str[i * cloud_bits:cloud_bits * (i + 1)]
    
    try:
      shuffle_arr.append(int(cur_input, 2))
    except:
      print(cur_input)

  fisher_yates(cloud_arr, shuffle_arr)

def hex_to_bin(hex):
  return bin(int(hex, 16))[2:].zfill(8)


def mouse_xor(mouse_bits, cloud_str_padded):
  cloud_arr = unpad(str(cloud_str_padded))

  shuffle_bits(mouse_bits, cloud_arr)
  # Concatenate all the bits in the array into a string
  cloud_str = ""
  res = "".zfill(2048)
  for i in cloud_arr:
    cloud_str += str(i)


  while res[0] != "1" or res[1024] != "1":
    start = random.randrange(
      0, len(cloud_str))  # Determine start of sliding window
    end = start + 2048

    if end > len(cloud_str) - 1:  # If sliding window exceeds pool of bits
      temp = cloud_str[(start - 2048):start]
      cloud_str_subset = temp[::-1]
    else:
      cloud_str_subset = cloud_str[start:end]

    # XOR cloud string subset with psuedo random 2048 bits number
    res = [
      str(int(cloud_str_subset[i]) ^ int(mouse_bits[i]))
      for i in range(len(cloud_str_subset))
    ]
    res = ''.join(res)

  print("Completed generating", len(res), "bits")
  print("MSB is", res[0])
  return res


def prime_gen(rand_num):

  print(f"Length of rand_num is {len(rand_num)}")
  pNum = rand_num[:int(len(rand_num) / 2)]
  qNum = rand_num[int(len(rand_num) / 2):]

  print(f"Length of pNum is {len(pNum)}")
  print(f"Length of qNum is {len(qNum)}")

  print(type(pNum))
  print(type(qNum))

  # Ensure pNum is odd
  if pNum[-1] == "0":
    pOdd = int(pNum, 2) + 1
  else:
    pOdd = int(pNum, 2)

  # Ensure qNum is odd
  if qNum[-1] == "0":
    qOdd = int(qNum, 2) + 1
  else:
    qOdd = int(qNum, 2)

  i = 0
  # Check whether odd_num is prime with security parameter == 40
  while (not rabin_miller(pOdd, 40)):
    i += 1
    pOdd += 2

  j = 0
  # Check whether odd_num is prime with security parameter == 40
  while (not rabin_miller(qOdd, 40)):
    j += 1
    qOdd += 2


  return bin(pOdd)[2:], bin(qOdd)[2:]


def rabin_miller(n, k):
  # If number is even, it's a composite number
  if n == 2:
    return True
  if n % 2 == 0:
    return False
  r, s = 0, n - 1
  while s % 2 == 0:
    r += 1
    s //= 2
  for _ in range(k):
    a = random.randrange(2, n - 1)
    x = pow(a, s, n)
    if x == 1 or x == n - 1:
      continue
    for _ in range(r - 1):
      x = pow(x, 2, n)
      if x == n - 1:
        break
    else:
      return False
  return True
  

#################### API ####################
class default(Resource):

  def get(self):
    print("Server active!")
    return "CZ4010"


class csprng(Resource):

  def get(self):
    print("GET request initiated")
    return csprng_weather()

  def post(self):
    print("POST request initiated")
    data = request.form
    mouse_bits = data['mouse_bits']
    padded_cloud_str = data['padded_cloud_str']

    # print(mouse_bits)
    # print(padded_cloud_str)
    res = mouse_xor(mouse_bits, padded_cloud_str)

    p,q = prime_gen(res)
    print(p)

    return [res, p, q]


# Creating API endpoints
api.add_resource(default, '/')
api.add_resource(csprng, '/api/csprng')


def run():
  app.run(host='0.0.0.0', port=7210)


t = Thread(target=run)
t.start()
