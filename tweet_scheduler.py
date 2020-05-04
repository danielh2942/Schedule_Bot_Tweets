import glob
import os
import schedule_tweet
from datetime import datetime, timedelta

def int_selection():
	return int(input("Your Choice: "))

#Schedule Tweet Data
username = "USERNAME"
password = "PASSWORD"

save_selected = 0
saves = glob.glob("saves/*.txt")
if (len(saves) > 0):
	print("A save file exists, Would you like to load it?\n1. Yes\n2. No")
	selection = int_selection()
	if (selection == 1):
		save_selected = 1
		print("Please pick a save")
		for i in range(0,len(saves)):
			print("%s %s"%(i,saves[i]))
		selection = int_selection()
		if (selection >= len(saves)):
			print("Does Not Exist!\nDefaulting...")
		else:
			save_file = open(saves[selection],"r")
			count = 0
			try:
				for x in save_file:
					if count == 0:
						temp = x
						temp = temp.replace("\n","")
						s_time = datetime.strptime(temp,'%Y-%m-%d %H:%M:%S')
					if count == 1:
						curr_file = x.replace("\n","")
					if count == 2:
						tweet_position = int(x)
					count = count + 1
			except ValueError as e:
				print(e)
				print("Failed")
				exit

else:
	#Time Handler
	print("What Time Would you like to set as the first time?\n1. Now\n2. Set Time")
	selection = int_selection()
	if (selection == 2):
		print("Set time of first tweet")
		while(True):
			print("Enter in the Format DD/MM/YYYY HH:MM:SS")
			time_string = input()
			try:
				s_time = datetime.strptime(time_string,'%d/%m/%Y %H:%M:%S')
			except ValueError as e:
				print("Invalid Format!")
				continue
			print("You entered The Time: %s Is This Correct \n1. Yes\n2. No"%(s_time))
			selection = int_selection()
			if (selection == 1):
				break
	else:
		s_time = datetime.now()

	doc_files = glob.glob("tweets/*.txt")
	print("Which of these would you like to open?")
	for i in range(0,len(doc_files)):
		print("%s: %s"%(i,doc_files[i]))
	#Tweet Loading
	selection = int_selection()
	d_select = selection
	curr_file = doc_files[selection]
curr_file = open(curr_file,"r")
tweets = []
for x in curr_file:
	if ("====================" not in x):
		#Removal of parts of the string
		curr_line = x[2:-3]
		tweets.append(curr_line)
print("File Opened Successfully!")

if (save_selected == 0):
	#User Prompts
	print("Would You Like to: ")
	print("1. Open from the start")
	print("2. Open from a certain Tweet?")
	selection = int_selection()
	tweet_position = 0
	if (selection == 2):
		selection = int_selection()
		tweet_position = selection

#Tweet Selection
print("y = schedule n = Refuse x = Quit")
scheduled = []
approved = 0
refused = 0
while(True):
	print("%s"%(tweets[tweet_position]))
	selection = input()
	if ("y" in selection):
		scheduled.append(tweets[tweet_position])
		approved = approved + 1
	elif ("n" in selection):
		refused = refused + 1
	elif (tweet_position == 999 or "x" in selection or approved == 300):
		if(tweet_position ==  999):
			print("File has been Exhausted!")
		break
	tweet_position = tweet_position + 1
if (approved == 0 and refused == 0):
	exit
#Tweet Dump
with schedule_tweet.session(username,password) as session:
	for i in scheduled:
		session.tweet(s_time,i)
		s_time = s_time + timedelta(minutes=30)
curr_file.close()
ratio = (approved/(approved+refused)) * 100
print("Current Position: %s, Approved: %s, Refused: %s, Percent Approved: %s%%" % (tweet_position,approved,refused,ratio))

if(tweet_position < 999):
	print("Would you like to save progress for another time?\n1. Yes\n 2. No")
	selection = int_selection()
	if (selection == 1):
		savename = "saves/savefile-{0}_{1}_{2}.txt".format(datetime.now().year,datetime.now().month,datetime.now().day)
		filesave = open(savename,"w")
		filesave.write("%s\n%s\n%s" % (s_time,doc_files[d_select],tweet_position))
		filesave.close()
