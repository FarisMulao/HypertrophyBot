import json
from datetime import datetime
import random

#-----------------------------------------------------------------------
#get the workout data from the file for a certain date and run the randomizations
def getWorkout(date):
  with open("workouts.json") as f:
    data = json.load(f)
  #when choosing workouts, we will seed the randomizer with the 
  #month, date, and year, so if this function is recalled, it 
  #will still generate the same randomization
  random.seed(date.strftime("%Y-%m-%d"))
  exerciseList = []
  for workout in data[date.strftime("%A")]:
    if len(workout.keys()) > 1:
      rand = random.random()
      weightSum = 0
      for key in workout.keys():
        if rand < workout[key] + weightSum:
          exerciseList.append(key)
          break
        else:
          weightSum += workout[key]
    else:
      exerciseList.append(list(workout.keys())[0])
  return exerciseList
#------------------------------------------------------------------

print(getWorkout(datetime.today()))



def printData(func):
  print("this ran before the function")
  func
  print("This ran after the function")

