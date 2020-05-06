import glob
import schedule_tweet
from datetime import datetime, timedelta

#GLOBALS
username = "USERNAME"
password = "PASSWORD"
curr_file = ""
doc_files = glob.glob("tweets/*.txt")
s_time = datetime.now()
tweet_position = 0
d_select = ""
scheduled = []
approved = 0
refused = 0
save_file = ""

def int_selection():
	while(1):
		try:
			selection = int(input("Your Value: "))
		except ValueError as e:
			print(e)
			continue
		return selection

def load(saves):
	global s_time
	global curr_file
	global tweet_position
	count = 0
	if(len(saves) == 1):
		print("Loading %s" % (saves[0]))
		save_file = saves[0]
	else:
		for i in range(0,len(saves)):
			print("%d %d" % (i,saves[i]))
		while(1):
			selection = int_selection()
			if(selection >= len(saves)):
				print("Out of range!")
			else:
				save_file = saves[selection]
				break
	curr_save = open(save_file,"r")
	try:
		for x in curr_save:
			if count == 0:
				s_time = datetime.strptime(x.replace("\n",""),'%Y-%m-%d %H:%M:%S')
			if count == 1:
				curr_file = x.replace("\n","")
			if count == 2:
				tweet_position = int(x)
			count = count + 1
	except ValueError as e:
		print(e)
		print("Defaulting")
		return 0
	print("Done!")
	return 1

def create():
	#Time
	global tweet_position
	global curr_file
	global d_select
	global s_time
	print("What Time Would you like to set as the first time?\n1. Now\n2. Set Time")
	selection = int_selection()
	if (selection == 2):
		print("Set time of first tweet")
		while(True):
			print("Enter in the Format DD/MM/YYYY HH:MM:SS")
			time_string = input()
			try:
				s_time = datetime.strptime(time_string,'%d/%m/%Y %H:%M:%S')
			except:
				print("Invalid Format!")
				continue
			print("You entered The Time: %s Is This Correct \n1. Yes\n2. No"%(s_time))
			selection = int_selection()
			if (selection == 1):
				break
	#Load Tweets
	doc_files = glob.glob("tweets/*.txt")
	print("Which of these would you like to open?")
	for i in range(0,len(doc_files)):
		print("%s: %s"%(i,doc_files[i]))
	#Pick Tweets
	selection = int_selection()
	d_select = selection
	curr_file = doc_files[selection]

	#User Prompts
	print("Would You Like to: ")
	print("1. Open from the start")
	print("2. Open from a certain Tweet?")
	selection = int_selection()
	if (selection == 2):
		selection = int_selection()
		tweet_position = selection

def load_tweets():
	global tweet_position
	global curr_file
	global approved
	global refused
	global scheduled
	read_file = open(curr_file,"r")
	tweets = []
	for x in read_file:
		if ("====================" not in x):
		#Removal of parts of the string
			curr_line = x[2:-3]
			tweets.append(curr_line)
	print("File Opened Successfully!")
	read_file.close()

	print("y = schedule n = Refuse x = Quit")
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

def upload():
	#Tweet Dump
	global approved
	global refused
	global scheduled
	global s_time
	with schedule_tweet.session(username,password) as session:
		for i in scheduled:
			session.tweet(s_time,i)
			s_time = s_time + timedelta(minutes=30)
	ratio = (approved/(approved+refused)) * 100
	print("Current Position: %s, Approved: %s, Refused: %s, Percent Approved: %s%%" % (tweet_position,approved,refused,ratio))

def main():
	save_selected = 0
	print("Tweet Scheduler Version 2\nWritten by Daniel Hannon")
	saves = glob.glob("saves/*.txt")
	if (len(saves) > 0):
		print("A minimum of one save file exists.\nWould you like to load it?\n1. Yes\n2. No")
		selection = int_selection()
		if(selection == 1):
			#Load Function
			save_selected = load(saves)

	if(save_selected == 0):	#Allows for Failure of load function
		#Create new Config
		create()

	load_tweets()
	upload()
	#save
	if(tweet_position < 999):
		print("Would you like to save progress for another time?\n1. Yes\n 2. No")
		selection = int_selection()
		if (selection == 1):
			savename = "saves/savefile-{0}_{1}_{2}.txt".format(datetime.now().year,datetime.now().month,datetime.now().day)
			filesave = open(savename,"w")
			if (save_selected == 0):
				filesave.write("%s\n%s\n%s" % (s_time,doc_files[d_select],tweet_position))
			else:
				filesave.write("%s\n%s\n%s" % (s_time,save_file,tweet_position))
			filesave.close()
	
main()
