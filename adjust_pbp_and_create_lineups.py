import math
import pandas as pd
df = pd.read_csv("data/regular/round_1/BAMvsTEL.csv")

def adjustments():
    # change col name to Jersey
    df.rename(columns={"DORSAL": "JERSEY"},inplace=True)

    # delete empty columns
    del df["COMMENT"]
    del df["TYPE"]

    # get the int(min), int(sec) from time
    df["Q_MIN"] = df["MARKERTIME"].apply(lambda row: 0 if type(row) != str else int(row.split(":")[0]))
    df["Q_SEC"] = df["MARKERTIME"].apply(lambda row: 0 if type(row) != str else int(row.split(":")[1]))
    
    # remove blanks from CODETEAM
    df["CODETEAM"] = df["CODETEAM"].apply(lambda row: row[0:3])

    # get the points scored at the play from the cummulative
    df["POINTS_A"].fillna(method='ffill', inplace = True) 
    df["POINTS_B"].fillna(method='ffill', inplace = True)
    df["POINTS_A"].fillna(0, inplace = True)
    df["POINTS_B"].fillna(0, inplace = True)
    df["SCORE_A"] = df["POINTS_A"].diff()
    df["SCORE_B"] = df["POINTS_B"].diff()
    df["SCORE_A"].fillna(0, inplace = True)
    df["SCORE_B"].fillna(0, inplace = True)
    
adjustments()

# store the team code name
team_a_code = df.iloc[0,13]
team_b_code = df.iloc[0,15]

# store the seperate dfs, the respective indices and the respective last indices of team 
team_a_df = df[df["CODETEAM"]==team_a_code]
team_a_indices = team_a_df.index
last_team_a_index = team_a_indices[-1]
team_b_df = df[df["CODETEAM"]==team_b_code]
team_b_indices = team_b_df.index
last_team_b_index = team_b_indices[-1]

# store the sub keywords and create empty lists of the substition points
sub_words = ["IN","OUT"]
team_a_sub_points, team_b_sub_points = [], []

# go through the dataframes one by one and find each substitution point by flagging each point
# where there is no substitution keyword after a substitution keyword
row_iterator = team_a_df.iterrows()
for index, row in row_iterator:
    if row["PLAYTYPE"] in sub_words:
        next_index = index + 1
        if next_index > last_team_a_index:
            break
        while next_index not in team_a_indices:
            next_index += 1
            if next_index > last_team_a_index:
                break
        if team_a_df.loc[next_index,"PLAYTYPE"] not in sub_words:
            team_a_sub_points.append(index)
        
row_iterator = team_b_df.iterrows()
for index, row in row_iterator:
    if row["PLAYTYPE"] in sub_words:
        next_index = index + 1
        if next_index > last_team_b_index:
            break
        while next_index not in team_b_indices:
            next_index += 1
            if next_index > last_team_b_index:
                break
        if team_b_df.loc[next_index,"PLAYTYPE"] not in sub_words:
            team_b_sub_points.append(index)

# create a dictionary to store the lineups in with a key being the subsitution point as found before
# go through all substitution points and effectively segment the dataframe in sub point to sub point
# while doing so, go through each segment and append every player to the lineup list if he has not been
# appended before or if he is getting in now.
# also store the players that are getting in and the ones that are getting out so you can pass along a 
# clean version of the lineup list in the next loop
team_a_lineups = {}
start = 0
player_lineup = []
in_lineup = []
out_lineup = []
for sub_point in team_a_sub_points:
    valid_indices = [item for item in team_a_indices if item >= start and item <= sub_point]
    for index in valid_indices:
        if type(team_a_df.loc[index, "PLAYER"]) is not str:
            continue
        
        if team_a_df.loc[index, "PLAYTYPE"] == "IN":
            in_lineup.append(team_a_df.loc[index, "PLAYER"])
            continue
        elif team_a_df.loc[index, "PLAYTYPE"] == "OUT":
            out_lineup.append(team_a_df.loc[index, "PLAYER"])
            
        if team_a_df.loc[index, "PLAYER"] not in player_lineup:
            player_lineup.append(team_a_df.loc[index, "PLAYER"])
        
    team_a_lineups[sub_point] = player_lineup
    
    player_lineup = [player for player in player_lineup if player not in out_lineup]
    player_lineup = player_lineup + in_lineup
    
    out_lineup, in_lineup = [],[]
    
    start = sub_point + 1
    
team_b_lineups = {}
start = 0
player_lineup = []
in_lineup = []
out_lineup = []
for sub_point in team_b_sub_points:
    valid_indices = [item for item in team_b_indices if item >= start and item <= sub_point]
    for index in valid_indices:
        if type(team_b_df.loc[index, "PLAYER"]) is not str:
            continue
        
        if team_b_df.loc[index, "PLAYTYPE"] == "IN":
            in_lineup.append(team_b_df.loc[index, "PLAYER"])
            continue
        elif team_b_df.loc[index, "PLAYTYPE"] == "OUT":
            out_lineup.append(team_b_df.loc[index, "PLAYER"])
            
        if team_b_df.loc[index, "PLAYER"] not in player_lineup:
            player_lineup.append(team_b_df.loc[index, "PLAYER"])
        
    team_b_lineups[sub_point] = player_lineup
    
    player_lineup = [player for player in player_lineup if player not in out_lineup]
    player_lineup = player_lineup + in_lineup
    
    out_lineup, in_lineup = [],[]
    
    start = sub_point + 1