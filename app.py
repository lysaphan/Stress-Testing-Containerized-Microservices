import time

import redis
from flask import Flask
from flask.json import jsonify

from math import sqrt

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379,decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def is_prime(n):
    if n % 2 == 0 or n <= 1:
        return False
    if n == 2:    
        cache.sadd("PrimeSet", n)
        return True

    sqr = int(sqrt(n)) + 1

    for div in range(3, sqr, 2):
        if n % div == 0: 
            return False
    cache.sadd("PrimeSet", n)
    return True

def get_primes_redis():
    primeList = cache.smembers("PrimeSet")
    return primeList
    
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<int:number>')
def isPrime(number):
    res = is_prime(number)
    if(res):
        return '{} is prime\n'.format(number)
    return '{} is not prime\n'.format(number)

@app.route('/primesStored')
def primesStored():
    listOfPrimes = list(get_primes_redis())
    return jsonify({'List of primes': listOfPrimes})

