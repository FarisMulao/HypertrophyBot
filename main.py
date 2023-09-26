
import discord
from discord.ext import tasks
import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from datetime import time
import random
import schedule


#-----------------------------------------------------------------------
#get the workout data from the file for a certain date and run the randomizations
#returns a string that includes the current date and the workouts in a nicely formatted list
def getWorkout(date: datetime):
  with open("workouts.json") as f:
    data = json.load(f)
  #when choosing workouts, we will seed the randomizer with the
  #month, date, and year, so if this function is recalled, it
  #will still generate the same randomization
  random.seed(date.strftime("%Y-%m-%d"))
  outString = "Workouts for " + date.strftime("%A, %m-%d-%y") + "\n"
  for count, workout in enumerate(data[date.strftime("%A")]):
    if len(workout.keys()) > 1:
      rand = random.random()
      weightSum = 0
      for key in workout.keys():
        if rand < workout[key] + weightSum:
          outString += str(count + 1) + ". " + key + "\n"
          break
        else:
          weightSum += workout[key]
    else:
      outString += str(count + 1) + ". " + list(workout.keys())[0] + "\n"
  return outString

def getAlt(muscle):
  with open("alternate.json") as g:
    dataAlt = json.load(g)
    output = "Alternates for " + muscle + "\n"
    for count, exercise in enumerate(dataAlt[muscle]):
      output += str(count + 1) + ". " + exercise + "\n"
    return output




#------------------------------------------------------------------

#Removed my bots token just in case
token = 'YOUR TOKEN'

#define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)


def do_nothing():
  print("hello")

@client.event
async def on_ready():
  printDailyWorkouts.start()
  await printDailyWorkouts()
  pass

@client.event
async def on_message(message):
  if message.application_id == client.application_id:
    return
  
  if message.content.startswith(".help"):
    await message.channel.send("Lizard 2 workout bot by Faris and Ethan\nTry .workouts to see what's todays workout!\nTry .alt to see alternate exercises!")

  if message.content.startswith(".test"):
    await message.channel.send(client.get_guild(1092003293280083988).get_channel(1092003436658163803))
  
  if message.content.startswith(".workouts"):
    #try to pull an int input
    try:
      dayModifier = int(message.content.split()[1])
    except:
      dayModifier = 0
    #for now, just call the function with the current date
    selectedTime = datetime.now(timezone(timedelta(hours=-5))) + timedelta(days=dayModifier)
    outString = getWorkout(selectedTime)  #convert to CST
    #outString = "Workouts for " + selectedTime.strftime("%A, %m-%d-%y") + "\n"
    #for count, i in enumerate(workoutList):    #this can be improved
    #  outString += str(count+1) + ". " + i + "\n"
    await message.channel.send(outString)
    
  if message.content.startswith(".alt"):
    try:
      muscle = (message.content.split()[1]).lower()
      await message.channel.send(getAlt(muscle))
    except:
      await message.channel.send("Not a muscle :(")

  tempCount = 0
  if message.content.startswith(".startDaily"):
    try:
      schedule.every(0.0001).hours.do(do_nothing())
    except:
      print("dont workie")
    while tempCount < 10:
      schedule.run_pending()
      tempCount += 1
      time.sleep(1)

@tasks.loop(time=time(hour=5, minute=1)) #time=time(hour=19, minute=6)
async def printDailyWorkouts(): #datetime.now(timezone(timedelta(hours=-5)))
  outString = getWorkout(datetime.now(timezone(timedelta(hours=-5))))
  await client.get_guild(1092003293280083988).get_channel(1092003436658163803).send(outString)



if __name__ == "__main__":
  client.run(token)
  
