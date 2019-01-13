# Description of files

The create_pbp_database.py file allows the user to easily create a database of the Euroleague 2017-2018 season play by play database locally. The database created by this file is in its rawest format so any analysis can be done on top of it.

The adjust_pbp_and_create_lineups.py file cleans up and also adds lineups to the original data.

The create_lineup_stats.py file creates statistics for all lineups. Specifically, it creates a dictionary with team names as keys. The values of these keys are dictionaries with lineups as keys. The value of these keys is a dictionary with the name of the stat line as a key. The value of that key is the value of that stat line.

The Cluster Lineups notebook performs the gathering of stats per lineups and writes a database of these stats. It later performs unsupervised Machine Learning and clusters lineups based on their stats (TBC).

# Data folder
In the data folder you can find the raw Euroleague play by play data in case you just want to donwload that directly. You can also find the adjusted (cleaning and lineup additions) data in the same folder under adjusted.

# How to use

Run the create_pbp_database.py file in a suitable directory. This will create all sub folders needed within that directory. If you need to adjust the files as well run the adjust_pbp_and_lineups.py file in the same directory and the adjustments will be made. If you want to create the statistics of all lineups run the create_lineup_stats.py file.

# Further work

If you do any work on top of this code and adjust the data from the raw form to something more useful, push the new py file to the repo and explain what kind of a format you are offering. 
