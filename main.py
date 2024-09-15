import os
import discord
from discord.ext import commands
import discord.utils
import json
import requests
from keep_alive import keep_alive
import random

my_secret = os.environ['TOKEN']

bot = commands.Bot(command_prefix='$')


#Confirmation that the bot is working and we are in the server already
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


#Messing with the bot
standard_replies = [
  "Nice",
  "Cool",
  "Suck on Deeznuts",
  "Good to Know",
  "Whatever",
  "Shut the fk up"
]


#getting qna data
def get_qna():
    response = requests.get('https://api.api-ninjas.com/v1/trivia?category=general', headers={'X-Api-Key': 'H9VqWuXMXDfrvEXVjyfA0Q==kzPSCTpti3VxRYVi'})
    json_data = json.loads(response.text)
    global question
    global answer
    question = json_data[0]['question'] + "?"
    answer = json_data[0]['answer']
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    return

    
#qna and messing with bot beature
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('$question'):
        get_qna()
        await message.channel.send(question)
    elif message.content.startswith('$answer'):
        await message.channel.send(answer)

    if bot.user.mentioned_in(message):
        await message.channel.send(random.choice(standard_replies))
    
    await bot.process_commands(message)
  

#Inspiring random quote feature
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    return(quote)

@bot.command(name='inspire', help='Sends a random inspirational quote')
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote) 

    
#Initiate a convo feature
@bot.command(name='bored', help='If ur bored n wanna talk just use lor')
async def bored(ctx):
    await ctx.send("@everyone GET UR ASSES IN THE SERVER LETS TALK") 

    
#Summon people to play feature
@bot.command(name='game', help='A tool to help Andi find gaming buddies')
async def GAME(ctx):
    await ctx.send("@everyone GET UR ASSES IN THE SERVER ANDI WANTS TO PLAY") 

    
#Planning feature
@bot.command(name='plan', help='A tool to help plan an outing wif da gang')
async def plan(ctx):
    await ctx.send("@everyone GET UR ASSES IN THE SERVER LETS GO OUT")    

    
#Resurrecting feature
@bot.command(name='resurrect', help='Bring back a dead member. Usage: $resurrect DeadBoi69')
async def resurrect(ctx, user: discord.Member):
    await ctx.send(f"{user.mention}GET UR ASS IN THE SERVER U ANTI SOCIAL PIECE OF SHIT")

    
#Messing around with elijah feature
@bot.command(name='skynet', help='A tool to attain world domination')
async def skynet(ctx):
    await ctx.send(file=discord.File('terminator-nope.gif'))  
    
#Baymax gif feature
baymax = os.path.join(os.getcwd(), "BaymaxGifs")

def select_random_image_path():
    return os.path.join(baymax, random.choice(os.listdir(baymax)))

@bot.command(name='sad', help='A lil surprise to cheer you up during your darkest times:)')
async def sad(ctx):
    await ctx.send(file=discord.File(select_random_image_path()))

    
#Polling Feature
@bot.command(name='poll', help='Helps you fkers make up ur mind. Usage: $poll "question" "option1" "option2"')
async def poll(ctx, question, *options: str):

    if len(options) > 2:
        await ctx.send('```Error! Syntax = [$poll "question" "option1" "option2"] ```')
        return

    if len(options) == 2 and options[0] == "yes" and options[1] == "no":
        reactions = ['👍', '👎']
    else:
        reactions = ['👍', '👎']

    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)

    poll_embed = discord.Embed(title=question, color=0x31FF00, description=''.join(description))

    react_message = await ctx.send(embed=poll_embed)

    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)


#Phrase counter feature
def load_counters():
    with open('counters.json', 'r') as f:
       counters = json.load(f)
    return counters

def save_counters(counters):
    with open('counters.json', 'w') as f:
       json.dump(counters, f)

class Message_Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        if 'wtf' in message.content.lower:
            counters = load_counters()
            counters['wtf'] += 1
            save_counters(counters)

def setup(bot):
    bot.add_cog(Message_Counter(bot))

def get_wtf():
    with open('counters.json', 'r') as f:
        json_data = json.load(f)
        wtf = json_data['wtf']
    return(wtf)

@bot.command(name='wtfcounter', help='How many times wtf has been said in this server')
async def wtfcounter(ctx):
    wtf = get_wtf()
    await ctx.send(f"Wtf was said {wtf} times")     

    
#Running the bot itself
keep_alive()

