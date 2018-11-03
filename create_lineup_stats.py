import os
import pandas as pd
import numpy as np
import re

# initialise empty dictionary
lineup_info = {}

# playtypes that will not be recorded
no_action_types = ["BP","EP","IN","OUT","TOUT","EG","SG","TOUT_TV"]

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

# go through all the data and create a dictionary that contains data on the lineups
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
                    play_type = row["PLAYTYPE"]
                    for lineup in lineup_info[home_team_code].keys():
                        if play_type not in lineup_info[home_team_code][lineup]:
                            if play_type not in no_action_types:
                                lineup_info[home_team_code][lineup][play_type] = 0
                    for lineup in lineup_info[away_team_code].keys():
                        if play_type not in lineup_info[away_team_code][lineup]:
                            if play_type not in no_action_types:
                                lineup_info[away_team_code][lineup][play_type] = 0

# find the total number of lineups                                 
total_lineups = {}
for key, value in lineup_info.items():
    d = lineup_info[key]
    l = len(d)
    total_lineups[key] = l
	
# go through all the data and create a dictionary that contains data on the lineups
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

            # add the playtypes as keys of the lineups dictionaries (if not already added)
            for i, row in df.iterrows():
                home_lineup, away_lineup = return_sorted_lineups(row)
                play_type = row["PLAYTYPE"].replace(" ", "")
                if play_type not in no_action_types:
                    if row["CODETEAM"] == home_team_code:
                        lineup_info[home_team_code][home_lineup][play_type] += 1
                        lineup_info[home_team_code][home_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
                    elif row["CODETEAM"] == away_team_code:
                        lineup_info[away_team_code][away_lineup][play_type] += 1
                        lineup_info[away_team_code][away_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]

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
                        elif row["CODETEAM"] == away_team_code:
                            lineup_info[away_team_code][away_lineup][play_type] += 1
                            lineup_info[away_team_code][away_lineup]["seconds"] += row["SECONDS_TO_NEXT_PLAY"]
							
# create a dictionary that contains lineup info only for lineups that played for 2 minutes or more together
min_sec = 120
for k,v in lineup_info.items():
        adjusted_lineup_info[k] = {key: value for key, value in lineup_info[k].items() if value["seconds"] >= min_sec}
        
# find the total number of adjusted lineups                                 
total_adjusted_lineups = {}
for key, value in adjusted_lineup_info.items():
    d = adjusted_lineup_info[key]
    l = len(d)
    total_adjusted_lineups[key] = l