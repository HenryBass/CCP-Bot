from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Server Up"

def run():
  app.run(host='0.0.0.0',port=8080)

def keepup():
    t = Thread(target=run)
    t.start()