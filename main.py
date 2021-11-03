import discord
import os
from replit import db
from keepup import keepup
import random

client = discord.Client()

good_words = ["hail ccp", "taiwan is not a country", "hail xi jinping", "hail the ccp", "i love china", "long live the ccp"]
swear_words = ["fuck", "shit", "pussy", "crap", "free speach"]
bad_words = ["taiwan is a country", "human rights", "capitalism", "winnie the pooh", "tibet is a part of china"]
sad_words = ["sad", "depressed", "bad", "sucks", "bored", "awful"]
happy_words = ["happy", "glad", "good", "great", "awesome"]

previous_message = ""

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content.lower()
  message_unaltered = message.content
  author = str(message.author)
  global previous_message

  if previous_message == msg:
    await message.channel.send("Message unoriginal! -20 social credits!!")
    db[author] = str(int(db[author]) - 20)
  elif msg in good_words:
    await message.channel.send("ALL HAIL CCP! +10 social credits!!")
    db[author] = str(int(db[author]) + 10)
    previous_message = msg
    print(previous_message, msg)
  elif any(word in msg for word in swear_words):
    await message.channel.send("No swearing! -25 social credits!!")
    db[author] = str(int(db[author]) - 25)
    previous_message = msg

  try:
    if int(db[author]) <= 0:
      await message.channel.send("Negative social credit score detected. SHAME!! SHAME!! SHAME!!")
  except:
    pass
  
  if any(word in msg for word in sad_words):
    await message.channel.send("Uhoh, sombody's in a bad mood! -5 social credits!!")
    db[author] = str(int(db[author]) - 5)

  if any(word in msg for word in happy_words):
    await message.channel.send("That's the spirit! +5 social credits!!")
    db[author] = str(int(db[author]) + 5)

  if any(word in msg for word in bad_words):
    if author not in db.keys():
      await message.channel.send("You don't seem to have an CCP account!\nUse the create command with the $ prefix to make one!")
    await message.channel.send("That's not very good! -50 social credits!!")
    db[author] = str(int(db[author]) - 25)
  
  if msg.startswith("$create"):
    if author not in db.keys():
      db[author] = "1000"
      await message.channel.send("Account created, +1000 Social Credits")
    else:
      await message.channel.send("Account already created, -10 Social Credits")
      db[author] = str(int(db[author]) - 100)

  if msg.startswith("$score"):
    score = db[str(author)]
    await message.channel.send(score)

  if msg.startswith("$lotto"):
    winnings = random.randrange(-100, 100)
    db[author] = str(int(db[author]) + winnings)
    await message.channel.send("You won: " + str(winnings))
  
  if msg.startswith("$beg"):  
    num = random.randrange(0, 10)
    if num == 5:
      db[author] = str(int(db[author]) + 50)
      await message.channel.send("Xi Jinping has blessed you with 50 social credits!")
    else:
      await message.channel.send("Xi Jinping ignores your request.")

  if msg.startswith("$balof"):
    user = message_unaltered.replace("$balof ", "")
    try:
      await message.channel.send("User balance: " + db[str(user)])
    except:
      await message.channel.send("User dosen't exist")


  if msg.startswith("$users"):
    await message.channel.send(db.keys())

  if msg.startswith("$help"):
    await message.channel.send(
      "Use $score to see your social credit score\n\nUse $create to create an account\n\nUse $lotto to try the lottery\n\nUse $users to see all users\n\nDo good things to gain points, do bad things to lose them.\n\nUse $beg to beg Xi Jinping for social credits\n\nUse $balof + a username to find their balance.\n\n***THE CCP STANDS WITH YOU!***"
    )

keepup()
client.run(os.getenv('TOKEN'))