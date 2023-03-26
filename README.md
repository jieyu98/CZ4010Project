# Cryptographically Secure Random Number Generator

Created by [Seah Jie Yu](https://github.com/jieyu98) and [Heng Chuan Song](https://github.com/Garrido98) as part of a graded coursework for NTU's CZ4010 Applied Cryptography.

Visit the website [here](https://jieyu98.github.io/Cryptographically-Secure-Random-Number-Generator/).

## Project Motivations and Aims

We want to create a web application that features a unique, one-of-a-kind random number generator that:
- Has high entropy,
- Utilizes physical elements
- Minimizes pseudorandom components 

And the most important thing - It must be cryptographically secure (i.e. suitable for cryptographic applications such as DHKE or RSA.)

The RNG comprises of 2 major components: Mouse movements and weather

## Abstract View of Algorithm 

![Algorithm](https://imgur.com/Fy8yTyG.png)

## Generating random bits from mouse movements

In our web application:
- There is a 256x256px box
- Users can move their mouse in the box to generate random bits
- Every time there is a change in horizontal or vertical direction, the script will take the x and y coordinates of the mouse pointer, convert them to binary, and concatenate them 
- This process repeats until a total of 2048 bits have been generated!


## Generating random bits from weather data

To get a k-bit long cloud data:
- First we scrape an image of the clouds over Singapore from www.weather.gov.sg
- Image is then converted into bytes
- We remove all the white spaces, then finally convert the bytes into binary

To create more entropy, we decided to shuffle the weather bits.
- Fisher-Yates Algorithm
- Utilize mouse bits from before

### Fisher-Yates Algorithm

Swaps last element with RANDOM element, and repeat process until fully shuffled.

- Extended mouse-bits with KECCAK Hash
- Split resultant string into portions of log2(len(weather_bits)) and append to shuffle_arr
- Random index = pop element and modulus with last_index

## Final Steps

Then a sliding window protocol is used to extract 2048-bits. If the index picked for sliding window causes the window to exceed the available pool of bits, it will retrieve bits in a reverse manner.

Finally, we do a simple XOR operation between mouse bits and cloud bits, and we get out final 2048-bit random number!

### Prime Generation

One of the many uses for true random numbers is to generate prime numbers.

We utilize the Rabin Miller method to check for primality, adding 2 to the the odd number iteratively till it becomes prime.
