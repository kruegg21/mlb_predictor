import pandas as pd
import helper_functions as hf

def combine_batting_pitching():
	###################################################
	# READS RAW BATTING DATA

	#NUM ROW:
	#354943
	#<class 'pandas.core.frame.DataFrame'>
	#Int64Index: 368137 entries, 0 to 368136
	#Data columns (total 32 columns):
	#Unnamed: 0    368137 non-null int64
	#Rank          368137 non-null int64
	#Player        368137 non-null object
	#Date          368137 non-null object
	#Team          368137 non-null object
	#Opp           368137 non-null object
	#Result        368137 non-null object
	#PA            368137 non-null int64
	#AB            368137 non-null int64
	#R             368137 non-null int64
	#H             368137 non-null int64
	#2B            368137 non-null int64
	#3B            368137 non-null int64
	#HR            368137 non-null int64
	#RBI           368137 non-null int64
	#BB            368137 non-null int64
	#IBB           310572 non-null float64
	#SO            368137 non-null int64
	#HBP           368137 non-null int64
	#SH            368137 non-null int64
	#SF            310572 non-null float64
	#ROE           368137 non-null int64
	#GDP           310572 non-null float64
	#SB            368137 non-null int64
	#CS            368137 non-null int64
	#WPA           368137 non-null float64
	#RE24          368137 non-null float64
	#aLI           311344 non-null float64
	#BOP           368137 non-null int64
	#Pos           368137 non-null object
	#DK            152256 non-null float64
	#FD            152256 non-null float64
	batting = pd.read_csv('full_batting_dataset.csv')
	hf.error_checking(batting, "RAW BATTING DATA", 0)
	###################################################

	###################################################
	# READS RAW PITCHING DATA

	#NUM ROW:
	#113030
	#<class 'pandas.core.frame.DataFrame'>
	#Int64Index: 116824 entries, 0 to 116823
	#Data columns (total 41 columns):
	#Unnamed: 0    116824 non-null int64
	#Rank          116824 non-null int64
	#Player        116824 non-null object
	#Date          116824 non-null object
	#Team          116824 non-null object
	#Opp           116824 non-null object
	#Result        116824 non-null object
	#AppDec        116824 non-null object
	#IP            116824 non-null float64
	#H             116824 non-null int64
	#R             116824 non-null int64
	#ER            116824 non-null int64
	#BB            116824 non-null int64
	#SO            116824 non-null int64
	#HR            116824 non-null int64
	#UER           116824 non-null int64
	#Pit           116812 non-null float64
	#Str           116812 non-null float64
	#GSc           29487 non-null float64
	#IR            87337 non-null float64
	#IS            87337 non-null float64
	#BF            116824 non-null int64
	#AB            116824 non-null int64
	#2B            116824 non-null int64
	#3B            116824 non-null int64
	#IBB           116824 non-null int64
	#HBP           116824 non-null int64
	#SH            116824 non-null int64
	#SF            116824 non-null int64
	#GDP           116824 non-null int64
	#SB            116824 non-null int64
	#CS            116824 non-null int64
	#PO            116824 non-null int64
	#BK            116824 non-null int64
	#WP            116824 non-null int64
	#ERA           116824 non-null object
	#WPA           116810 non-null float64
	#RE24          116811 non-null float64
	#aLI           116810 non-null float64
	#DK            59058 non-null float64
	#FD            59058 non-null float64
	pitching = pd.read_csv('full_pitching_dataset.csv')
	hf.error_checking(pitching, "RAW PITCHING DATA", 0)
	#########################################################



	# CREATE PITCHING FEATURES ############################
	# remove relief and backup pitcher from set
	starting = pitching['AppDec'].str[0]
	pitching = pitching[~starting.str.isnumeric()]

	# numeric date and game number
	pitching = hf.add_numeric_date(pitching)
	pitching = hf.calculate_game_number(pitching, "Player")

	# gets averages
	pitching = pitching.sort_values(by = ["Player","Date"])
	pitching = hf.get_averages(pitching, "SO", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "BB", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "HR", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "Str", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "SB", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "H", "Pitcher", "PlayerGameNumber")
	pitching = hf.get_averages(pitching, "R", "Pitcher", "PlayerGameNumber")

	#######################################################

	# CREATE BATTING FEATURES #############################
	# numeric date and game number
	batting = hf.add_numeric_date(batting)
	batting = hf.calculate_game_number(batting, "Player")

	# gets averages
	batting = batting.sort_values(by = ["Player","Date"])
	batting = hf.get_averages(batting, "SO", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "BB", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "HR", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "H", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "R", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "SB", "Batter", "PlayerGameNumber")
	batting = hf.get_averages(batting, "CS", "Batter", "PlayerGameNumber")

	# one-hot encode park playing in
	team_list = ['TBD', 'TEX', 'ANA', 'STL', 'ATL', 'FLA','HOU', 'ARI', 'NYY', 
			 'BAL', 'CHW', 'DET', 'CLE', 'BOS', 'SDP', 'LAD','CHC', 'MIL', 
			 'KCR', 'MIN', 'NYM', 'WSN', 'PHI', 'PIT','CIN', 'OAK','SEA', 
			 'COL', 'SFG', 'TOR']
	for i in team_list:
		batting["On" + i] = batting.Team == i
		batting["On" + i] = batting.loc[:,"On" + i].astype(int)
		batting["Against" + i] = batting.Opp == i
		batting["Against" + i] = batting.loc[:,"Against" + i].astype(int)	
		batting["PlayingIn" + i] = batting.loc[:,"On" + i] * batting.Home + \
								   batting.loc[:,"Against" + i] * (~batting.Home + 2)

	# city game is held in
	batting["HomeTeam"] = batting.Home * batting.Team + (~batting.Home + 2) * batting.Opp

	# add airport code to merge weather data
	team_to_airport = {
		'SFG' : 'KSFO',
		'LAD' : 'KBUR',
		'OAK' : 'KOAK',
		'CLE' : 'KCLE',
		'SDP' : 'KSAN',
		'SEA' : 'KSEA',
		'BOS' : 'KBOS',
		'LAA' : 'KSNA',
		'ARI' : 'KPHX',
		'BAL' : 'KBWI',
		'CHC' : 'KMDW',
		'STL' : 'KSTL',
		'ATL' : 'KATL',
		'WSN' : 'KIAD',
		'HOU' : 'KIAH',
		'CIN' : 'KCVG',
		'KCR' : 'KMCI',
		'DET' : 'KDTW',
		'PHI' : 'KPHL',
		'MIL' : 'KMKE',
		'MIA' : 'KMIA',
		'NYM' : 'KLGA',
		'COL' : 'KDEN',
		'PIT' : 'KPIT',
		'FLA' : 'KMIA',
		'MIN' : 'KMSP',
		'CHW' : 'KMDW',
		'TOR' : 'CYYZ',
		'NYY' : 'KLGA',
		'TBR' : 'KTPA',
		'TEX' : 'KAWO',
	}

	ta = pd.DataFrame([[col1, col2] for col1, col2 in team_to_airport.items()], columns = ['HomeTeam', 'AirportCode'])
	batting = pd.merge(batting, ta, on = 'HomeTeam')
	hf.error_checking(batting, "FEATURES BUILT BATTING DATA", 0)

	# add weather data
	weather = pd.read_csv('full_weather.csv')
	batting = pd.merge(batting, weather, on = ['Date','AirportCode'], how = 'left')

	# missing weather data for scattering of days
	batting = batting[batting.loc[:,"MaxTemp"].notnull()]

	hf.error_checking(batting, "FEATURES BUILT BATTING DATA", 0)
	#######################################################

	#######################################################
	# MERGE PITCHING AND BATTING:
	# edits the name of pitching columns to prevent overlap with hitting columns
	pitching["BattingTeam"] = pitching.Opp
	pitching["OpposingPitcher"] = pitching.Player
	batting["BattingTeam"] = batting.Team
	pitching["PitAB"] = pitching.AB
	pitching["PitR"] = pitching.R
	pitching["PitH"] = pitching.H
	pitching["Pit2B"] = pitching.loc[:,"2B"]
	pitching["Pit3B"] = pitching.loc[:,"3B"]
	pitching["PitHR"] = pitching.HR
	pitching["PitBB"] = pitching.BB
	pitching["PitIBB"] = pitching.IBB
	pitching["PitSO"] = pitching.SO
	pitching["PitHBP"] = pitching.HBP
	pitching["PitSF"] = pitching.SF
	pitching["PitSH"] = pitching.SH
	pitching["PitSB"] = pitching.SB		
	pitching["PitGDP"] = pitching.GDP			
	pitching["PitCS"] = pitching.CS
	pitching["PitWPA"] = pitching.WPA
	pitching["PitRE24"] = pitching.RE24
	pitching["PitaLI"] = pitching.aLI
	pitching["PitDK"] = pitching.DK
	pitching["PitFD"] = pitching.FD
	pitching["PitcherPlayerGameNumber"] = pitching.PlayerGameNumber
	pitching.drop(["AB","R","H","2B","3B","HR","BB","IBB","SO",
			   "HBP","SH","SF","SB","GDP","CS","WPA",
			   "RE24","aLI","DK","FD","Opp","Player","Team","PlayerGameNumber"], 1, inplace = True)
	hf.error_checking(pitching, "EDITED PITCHING DATA", 0)
	full = pd.merge(batting, pitching, on = ['BattingTeam','Date'])

	# UPKEEP:
	full["Result"] = full.Result_x
	full["NumericDate"] = full.NumericDate_x
	full.drop(["Unnamed: 0_x", "Rank_x", "Result_x", "Result_y", "Rank_y", 
			   "Unnamed: 0_y", "NumericDate_x", "NumericDate_y"], 1, inplace = True)

	# one game does not have a starting pitcher (April, 4 MIN vs. CHW), so remove this game
	full = full[full.loc[:,"OpposingPitcher"].notnull()]
	hf.error_checking(full, "MERGED BATTING AND PLAYER", 1)
	#######################################################


	#######################################################
	# FULL DATASET
	#NUM ROW:
	#354931
	#Player 0 0 0
	#Date 0 0 0
	#Team 0 0 0
	#Opp 0 0 0
	#PA 0 0 0
	#AB 0 0 0
	#R 0 0 0
	#H 0 0 0
	#2B 0 0 0
	#3B 0 0 0
	#HR 0 0 0
	#RBI 0 0 0
	#BB 0 0 0
	#IBB 54725 0 0
	#SO 0 0 0
	#HBP 0 0 0
	#SH 0 0 0
	#SF 54725 0 0
	#ROE 0 0 0
	#GDP 54725 0 0
	#SB 0 0 0
	#CS 0 0 0
	#WPA 0 0 173600
	#RE24 0 0 176152
	#aLI 53972 0 90
	#BOP 0 0 0
	#Pos 0 0 0
	#DK 207505 0 159
	#FD 207505 0 40420
	#PlayerGameNumber 0 0 0
	#L1BatterSO 0 2379 2379
	#L2BatterSO 0 4671 4671
	#L3BatterSO 0 6882 6882
	#L5BatterSO 0 11133 11133
	#L10BatterSO 0 20877 20877
	#L20BatterSO 0 37875 37875
	#L50BatterSO 0 79503 79503
	#L1BatterBB 0 2379 2379
	#L2BatterBB 0 4671 4671
	#L3BatterBB 0 6882 6882
	#L5BatterBB 0 11133 11133
	#L10BatterBB 0 20877 20877
	#L20BatterBB 0 37875 37875
	#L50BatterBB 0 79503 79503
	#L1BatterHR 0 2379 2379
	#L2BatterHR 0 4671 4671
	#L3BatterHR 0 6882 6882
	#L5BatterHR 0 11133 11133
	#L10BatterHR 0 20877 20877
	#L20BatterHR 0 37875 37875
	#L50BatterHR 0 79503 79503
	#BattingTeam 0 0 0
	#AppDec 0 0 0
	#IP 0 0 0
	#ER 0 0 0
	#UER 0 0 0
	#Pit 14 0 0
	#Str 14 0 0
	#GSc 0 0 463
	#IR 354931 0 0
	#IS 354931 0 0
	#BF 0 0 0
	#PO 0 0 0
	#BK 0 0 0
	#WP 0 0 0
	#ERA 0 0 0
	#L1PitcherSO 0 7793 7793
	#L2PitcherSO 0 14907 14907
	#L3PitcherSO 0 21616 21616
	#L5PitcherSO 0 34167 34167
	#L10PitcherSO 0 61614 61614
	#L20PitcherSO 0 106055 106055
	#L50PitcherSO 0 203954 203954
	#L1PitcherBB 0 7793 7793
	#L2PitcherBB 0 14907 14907
	#L3PitcherBB 0 21616 21616
	#L5PitcherBB 0 34167 34167
	#L10PitcherBB 0 61614 61614
	#L20PitcherBB 0 106055 106055
	#L50PitcherBB 0 203954 203954
	#L1PitcherHR 0 7793 7793
	#L2PitcherHR 0 14907 14907
	#L3PitcherHR 0 21616 21616
	#L5PitcherHR 0 34167 34167
	#L10PitcherHR 0 61614 61614
	#L20PitcherHR 0 106055 106055
	#L50PitcherHR 0 203954 203954
	#OpposingPitcher 0 0 0
	#PitAB 0 0 0
	#PitR 0 0 0
	#itH 0 0 0
	#Pit2B 0 0 0
	#Pit3B 0 0 0
	#PitHR 0 0 0
	#PitBB 0 0 0
	#PitIBB 0 0 0
	#PitSO 0 0 0
	#PitHBP 0 0 0
	#PitSF 0 0 0
	#PitSH 0 0 0
	#PitSB 0 0 0
	#PitGDP 0 0 0
	#PitCS 0 0 0
	#PitWPA 35 0 174343
	#PitRE24 35 0 163478
	#PitaLI 35 0 0
	#PitDK 178167 0 28646
	#PitFD 178167 0 8295
	#PitcherPlayerGameNumber 0 0 0
	#Result 0 0 0
	#NumericDate 0 0 0
	#######################################################



	#######################################################
	# DUMP TO CSV:
	# makes test set:
	test = full[full.loc[:,"NumericDate"] > 5200]

	for i in full.columns:
		print "\"" + i + "\""

	# dumps test and full set
	test.to_csv('combined_batting_player_test.csv', index = False)
	full.to_csv('combined_batting_player.csv', index = False)
	#######################################################