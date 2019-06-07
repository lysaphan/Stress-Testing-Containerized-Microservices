import re
import unittest
import urlparse
import urllib2

PASS = re.compile(r"(\d+) is prime")
FAIL = re.compile(r"(\d+) is not prime")

def load(page):
  url = urlparse.urljoin("http://localhost:02691", page)
  try:
    req = urllib2.urlopen(url)
    return {"code": req.getcode(), "content": req.read()}
  except urllib2.HTTPError, e:
    return {"code": e.code, "content": None}


class TestURL(unittest.TestCase):
  def noPrime(self):
    self.assertEquals(load_page("isPrime")["code"], 404)

  def randomPrimes(self):
    self.assertRegexpMatches(load_page("isPrime/1")["content"], FAIL)
    self.assertRegexpMatches(load_page("isPrime/2")["content"], PASS)

  def storedPrimes(self):
    foundPrimes = set()
    for i in range(300):
      req = load_page("isPrime/" + str(i))
      self.assertEquals(req["code"], 200)
      if PASS.match(req["content"]) != None:
        foundPrimes.add(i)
    req = load("primesStored")
    self.assertEquals(req["code"], 200)
    numbers = req["content"].split(", ")
    stored = set()
    for val in number:
      stored.add(int(val))
    self.assertTrue(foundPrimes.issubset(stored))

unittest.main()
