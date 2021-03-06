"""Import needed modules"""
from bs4 import BeautifulSoup
import urllib.request as urllib2
import json
import pandas as pd
import os


def obtain_data(round, game_range):
	"""This function runs for a given range of games in a round of the Euroleague Season"""
	"""and creates a local database of the play by play data. It does so by first scraping"""
	"""the online database of Euroleague and then making some adjustments to fit all data"""
	"""in one dataframe. The last part of the code runs only to store the data locally"""
	for g in range(game_range[0], game_range[1]):

		url = "http://live.euroleague.net/api/PlayByPlay?gamecode=" + str(g) + "&seasoncode=E2017&disp="

		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

		hdr = {'User-Agent':user_agent,}

		req = urllib2.Request(url, headers=hdr)

		content = urllib2.urlopen(req).read()

		soup = BeautifulSoup(content,features="html5lib")

		data = json.loads(soup.prettify().split("\n")[4])

		home_team = data['TeamA']
		away_team = data['TeamB']
		home_team_code = data['CodeTeamA']
		away_team_code = data['CodeTeamB']
		overtime_boolean = data['ActualQuarter'] - 4 #actual quarter indicates number of quarters
		first_quarter = data['FirstQuarter']
		second_quarter = data['SecondQuarter']
		third_quarter = data['ThirdQuarter']
		fourth_quarter = data['ForthQuarter']
		extra_time = data['ExtraTime']

		df1 = pd.DataFrame(first_quarter)
		df2 = pd.DataFrame(second_quarter)
		df3 = pd.DataFrame(third_quarter)
		df4 = pd.DataFrame(fourth_quarter)
		frames = [df1,df2,df3,df4]
		full_game = pd.concat(frames)
		full_game["home_team"] = home_team
		full_game["home_team_code"] = home_team_code[0:3]
		full_game["away_team"] = away_team
		full_game["away_team_code"] = away_team_code[0:3]

		game_name = home_team_code[0:3] + 'vs' + away_team_code[0:3]
		
		"""From this point on, the data is being stored locally"""
		if round == "regular":
			round_of_game = ((g-1)// 8) + 1
			if not os.path.exists("data/raw/" + round + "/round_" + str(round_of_game)):
				os.makedirs("data/raw/" + round + "/round_" + str(round_of_game))
			path = "data/raw/" + round + "/round_" + str(round_of_game) + "/" 
		elif round == "playoff":
			round_of_game = ((g-241)// 4) + 1
			if not os.path.exists("data/raw/" + round + "/round_" + str(round_of_game)):
				os.makedirs("data/raw/" + round + "/round_" + str(round_of_game))
			path = "data/raw/" + round + "/round_" + str(round_of_game) + "/" 
		else: 
			if not os.path.exists("data/raw/" + round + "/"):
				os.makedirs("data/raw/" + round + "/")
			path = "data/raw/" + round + "/"
		
		full_name = path + game_name + ".csv"

		full_game.to_csv(full_name, index = False)
				
	return
		
"""These statements run the code, comment them if you don't want them to run"""
obtain_data("regular", (1,241))
obtain_data("playoff", (241,257))
obtain_data("f4", (257,261))