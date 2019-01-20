import os
import pandas as pd
import numpy as np
import re
import sys

# initialise empty dictionary
lineup_info = {}

# playtypes that will not be recorded
# acion types info in the list order
# begin period, end period, sub in, sub out, time out, end game, start_game, tv time out, tip off
# coaches fould, technical foul, bench foul, disqualifying foul
no_action_types = ["BP","EP","IN","OUT","TOUT","EG","SG","TOUT_TV","TPOFF","C","CMT","B","CMD"]


# helper function that returns the lineups as sorted lists
def return_sorted_lineups(row):
    home, away = [], []
    home.append(row["home_team_player_1"])
    home.append(row["home_team_player_2"])
    home.append(row["home_team_player_3"])
    home.append(row["home_team_player_4"])
    home.append(row["home_team_player_5"])
    away.append(row["away_team_player_1"])
    away.append(row["away_team_player_2"])
    away.append(row["away_team_player_3"])
    away.append(row["away_team_player_4"])
    away.append(row["away_team_player_5"])
    home, away = tuple(sorted(home)), tuple(sorted(away))
    return home, away

# go through all the data and create a dictionary that contains info on the lineups
data_path = "../data/adjusted_with_lineups/"
slash = "/"
season_parts = os.listdir(data_path) # generate the three distinct parts of the season (reg,pf,f4)
for part in season_parts:
    if part[0]==".":
        continue # if any hidden folders/files continue
    elif part[0]=="f": # meaning final4
        final_four = os.listdir(data_path + part + slash)
        for game in final_four:
            if '.csv' not in game: # again, avoid hidden files
                continue
            df = pd.read_csv(data_path + part + slash + game) # read, adjust, generate lineups, save with same name

            # add the home and away teams as keys (if they are not already added)
            home_team_code = df.loc[0,"home_team_code"]
            away_team_code = df.loc[0,"away_team_code"]
            if home_team_code not in lineup_info:
                lineup_info[home_team_code] = {}
            if away_team_code not in lineup_info:
                lineup_info[away_team_code] = {}
                
            # add the lineups as keys of the team dictionaries (if not already added)
            for i, row in df.iterrows():
                h, a = return_sorted_lineups(row)
                if h not in lineup_info[home_team_code]:
                    lineup_info[home_team_code][h] = {}
                    lineup_info[home_team_code][h]["seconds"] = 0
                if a not in lineup_info[away_team_code]:
                    lineup_info[away_team_code][a] = {}
                    lineup_info[away_team_code][a]["seconds"] = 0
                    
            # add the playtypes as keys of the lineups dictionaries (if not already added)
            for i, row in df.iterrows():
                play_type = row["PLAYTYPE"]
                for lineup in lineup_info[home_team_code].keys():
                    if play_type not in lineup_info[home_team_code][lineup]:
                        if play_type not in no_action_types:
                            lineup_info[home_team_code][lineup][play_type] = 0
                for lineup in lineup_info[away_team_code].keys():
                    if play_type not in lineup_info[away_team_code][lineup]:
                        if play_type not in no_action_types:
                            lineup_info[away_team_code][lineup][play_type] = 0     
                
    else:
        not_final_four = os.listdir(data_path + part + slash) # one layer more here as there are rounds
        for season_round in not_final_four:
            games_of_round = os.listdir(data_path + part + slash + season_round + slash)
            for game in games_of_round:
                if '.csv' not in game:
                    continue
                df = pd.read_csv(data_path + part + slash + season_round + slash + game)
                
                
                # add the home and away teams as keys (if they are not already added)
                home_team_code = df.loc[0,"home_team_code"]
                away_team_code = df.loc[0,"away_team_code"]
                if home_team_code not in lineup_info:
                    lineup_info[home_team_code] = {}
                if away_team_code not in lineup_info:
                    lineup_info[away_team_code] = {}

                # add the lineups as keys of the team dictionaries (if not already added)
                for i, row in df.iterrows():
                    h, a = return_sorted_lineups(row)
                    if h not in lineup_info[home_team_code]:
                        lineup_info[home_team_code][h] = {}
                        lineup_info[home_team_code][h]["seconds"] = 0
                    if a not in lineup_info[away_team_code]:
                        lineup_info[away_team_code][a] = {}
                        lineup_info[away_team_code][a]["seconds"] = 0

                # add the playtypes as keys of the lineups dictionaries (if not already added)
                for i, row in df.iterrows():
                    play_type = row["PLAYTYPE"].replace(" ", "")
                    for lineup in lineup_info[home_team_code].keys():
                        if play_type not in lineup_info[home_team_code][lineup]:
                            if play_type not in no_action_types:
                                lineup_info[home_team_code][lineup][play_type] = 0
                    for lineup in lineup_info[away_team_code].keys():
                        if play_type not in lineup_info[away_team_code][lineup]:
                            if play_type not in no_action_types:
                                lineup_info[away_team_code][lineup][play_type] = 0
								
# go through all the dictionaries and add the stats to the respective lineups
data_path = "../data/adjusted_with_lineups/"
slash = "/"
season_parts = os.listdir(data_path) # generate the three distinct parts of the season (reg,pf,f4)
for part in season_parts:
    if part[0]==".":
        continue # if any hidden folders/files continue
    elif part[0]=="f": # meaning final4
        final_four = os.listdir(data_path + part + slash)
        for game in final_four:
            if '.csv' not in game: # again, avoid hidden files
                continue
            df = pd.read_csv(data_path + part + slash + game) # read, adjust, generate lineups, save with same name
            

            # set the home and away team code
            home_team_code = df.loc[0,"home_team_code"]
            away_team_code = df.loc[0,"away_team_code"]            

            # add +1 & + minutes to the right lineup
            for i, row in df.iterrows():
                home_lineup, away_lineup = return_sorted_lineups(row)
                play_type = row["PLAYTYPE"].replace(" ", "")
                if play_type not in no_action_types:
                    if row["CODETEAM"] == home_team_code:
                        lineup_info[home_team_code][home_lineup][play_type] += 1
                        lineup_info[home_team_code][home_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
                        # if it is a made shot, need to declare it as an attempted as well
                        if play_type == "FTM":
                            lineup_info[home_team_code][home_lineup]["FTA"] += 1
                        if play_type == "2FGM":
                            lineup_info[home_team_code][home_lineup]["2FGA"] += 1
                        if play_type == "3FGM":
                            lineup_info[home_team_code][home_lineup]["3FGA"] += 1						
                    elif row["CODETEAM"] == away_team_code:
                        lineup_info[away_team_code][away_lineup][play_type] += 1
                        lineup_info[away_team_code][away_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
                        if play_type == "FTM":
                            lineup_info[away_team_code][away_lineup]["FTA"] += 1
                        if play_type == "2FGM":
                            lineup_info[away_team_code][away_lineup]["2FGA"] += 1
                        if play_type == "3FGM":
                            lineup_info[away_team_code][away_lineup]["3FGA"] += 1

    else:
        not_final_four = os.listdir(data_path + part + slash) # one layer more here as there are rounds
        for season_round in not_final_four:
            games_of_round = os.listdir(data_path + part + slash + season_round + slash)
            for game in games_of_round:
                if '.csv' not in game:
                    continue
                df = pd.read_csv(data_path + part + slash + season_round + slash + game)
                
                # add the home and away teams as keys (if they are not already added)
                home_team_code = df.loc[0,"home_team_code"]
                away_team_code = df.loc[0,"away_team_code"]
                # add the playtypes as keys of the lineups dictionaries (if not already added)
                for i, row in df.iterrows():
                    home_lineup, away_lineup = return_sorted_lineups(row)
                    play_type = row["PLAYTYPE"].replace(" ", "")
                    if play_type not in no_action_types:
                        if row["CODETEAM"] == home_team_code:
                            lineup_info[home_team_code][home_lineup][play_type] += 1
                            lineup_info[home_team_code][home_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
                            if play_type == "FTM":
                                lineup_info[home_team_code][home_lineup]["FTA"] += 1
                            if play_type == "2FGM":
                                lineup_info[home_team_code][home_lineup]["2FGA"] += 1
                            if play_type == "3FGM":
                                lineup_info[home_team_code][home_lineup]["3FGA"] += 1
                        elif row["CODETEAM"] == away_team_code:
                            lineup_info[away_team_code][away_lineup][play_type] += 1
                            lineup_info[away_team_code][away_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
                            if play_type == "FTM":
                                lineup_info[away_team_code][away_lineup]["FTA"] += 1
                            if play_type == "2FGM":
                                lineup_info[away_team_code][away_lineup]["2FGA"] += 1
                            if play_type == "3FGM":
                                lineup_info[away_team_code][away_lineup]["3FGA"] += 1
							
# find the total number of lineups                                 
total_lineups = {}
for key, value in lineup_info.items():
    d = lineup_info[key]
    l = len(d)
    total_lineups[key] = l
	
# create a dictionary that contains lineup info only for lineups that played for 5 minutes or more together
adjusted_lineup_info = {}
min_sec = 300
for k,v in lineup_info.items():
        adjusted_lineup_info[k] = {key: value for key, value in lineup_info[k].items() if value["seconds"] >= min_sec}
		
# find the total number of adjusted lineups                                 
total_adjusted_lineups = {}
for key, value in adjusted_lineup_info.items():
    d = adjusted_lineup_info[key]
    l = len(d)
    total_adjusted_lineups[key] = l
	
# place the keys of the dictionary (teams) as a value of the lineups
for k,v in adjusted_lineup_info.items():
    for ke,va in v.items():
        va["TEAM"] = k
		
# unpack the first layer of the dictionary (as the team is now stored as a value)
all_lineups = {}
for k, v in adjusted_lineup_info.items():
    for ke,va in v.items():
        all_lineups[ke]=va
		
# create a dataframe out of this dictionary
df = pd.DataFrame(all_lineups).T
df.reset_index(inplace=True, drop=False)
df.rename(columns = {"level_0":"player1", "level_1":"player2", "level_2":"player3", "level_3":"player4", "level_4":"player5"}, inplace = True)

# store this dataframe as this is the data that will be used for clustering
df.to_csv("../data/lineup_stats.csv", index = False)

