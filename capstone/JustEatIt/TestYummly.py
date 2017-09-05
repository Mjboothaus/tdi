import yummly

# default option values
TIMEOUT = 15.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'

client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

search = client.search('green eggs and ham')
match = search.matches[0]

match.id

recipe = client.recipe(match.id)

print recipe
