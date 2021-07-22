import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']
client = discord.Client()

if "responding" not in db.keys():
    db["responding"] = True

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote=json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
        print(db["encouragements"])
    else:
        db["encouragements"] = [encouraging_message]
        print(db["encouragements"])
    
def delete_encouragements(index):
    encouragements = db["encouragements"]
    if len(encouragements)>index:
        del encouragements[index]
        db["encouragements"]=encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    starter_encourangements= [ "You are a great person","Hang in there","You are the king","You are a tiger","Cheer Up","Stay Motivated"]
    sad_words = ["sad","depressed","unhappy","angry","depressing","depression","stressed","stress","moody"]

    if message.author == client.user:
        return

    msg=message.content

    if msg.startswith('$hello'):
        await message.channel.send('Hello!')

    if msg.startswith('$bye'):
        await message.channel.send('Byeee!!! See you soon...')
    
    if msg.startswith('$inspire'):
        quote=get_quote()
        await message.channel.send(quote)
    if db["responding"]:
        options = starter_encourangements
        if "encouragements" in db.keys():
            options = options.extend(db["encouragements"])

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(starter_encourangements))
    
    if msg.startswith('$new'):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added!!!")
    
    if msg.startswith("$del"):
        encouragements=[]
        if "encouragements" in db.keys():
            index = int(msg.split("$del",1)[1])
            encouragements = db["encouragements"]
            await message.channel.send("Deleted-: ")
            await message.channel.send(encouragements[index])
            delete_encouragements(index)
    if msg.startswith("$list"):
        encouragements=[]
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
    
    if msg.startswith("$responding"):
        value = msg.split("$responding",1)[1]
        print(value)
        if value.lower()==" true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))