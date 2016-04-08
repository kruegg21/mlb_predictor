import pandas as pd
import numpy as np

def build_xgboost_datasets(df, stat, stat_name, columns):
	# sort df by player and date and rename indexes
	nrows = len(df.index)
	df = df.sort_values(by = ["Player","Date"])
	df.index = xrange(nrows)

	# pick dataset with only relevent columns
	f_dataset = df.loc[:,columns]
	f_dataset.index = xrange(len(f_dataset.index))

	# replace NA with -999
	f_dataset[f_dataset.isnull()] = -999

	# DIVIDE INTO TRAIN AND CV:
	# 80-20 splits
	print len(f_dataset.index)
	f_dataset = f_dataset.sort_values(by = 'NumericDate')
	# f_dataset = f_dataset.iloc[:int(np.floor(nrows / 100))]
	print len(f_dataset.index)
	nrows = len(f_dataset.index)
	f_dataset.index = xrange(nrows)

	f_cv = f_dataset.iloc[int(np.floor(nrows * .8)):]
	f_train = f_dataset.iloc[:int(np.floor(nrows * .8))]



	# get labels for both cross validation and training sets
	f_cv_label = f_cv.loc[:,stat]
	f_train_label = f_train.loc[:,stat]

	# remove label from train and cross validation sets
	f_train = f_train.drop(stat,1)
	f_cv = f_cv.drop(stat,1)

	cv_set_file_name = 'final_' + str(stat_name) + '_cv.csv'
	train_set_file_name = 'final_' + str(stat_name) + '_train.csv'
	cv_set_label_file_name = 'final_' + str(stat_name) + '_cv_label.csv'
	train_set_label_file_name = 'final_' + str(stat_name) + '_train_label.csv'
	cv_full_file_name = 'final_' + str(stat_name) + '_cv_full.csv'
	train_full_file_name = 'final_' + str(stat_name) + '_train_full.csv'

	f_cv.to_csv(cv_set_file_name, index = False)
	f_train.to_csv(train_set_file_name, index = False)
	f_cv_label.to_csv(cv_set_label_file_name, index = False)
	f_train_label.to_csv(train_set_label_file_name, index = False)
	f_cv.to_csv(cv_full_file_name, index = False)
	f_train.to_csv(train_full_file_name, index = False)

	return

'''
"Player"
"Date"
"Team"
"Opp"
"PA"
"AB"
"R"
"H"
"2B"
"3B"
"HR"
"RBI"
"BB"
"IBB"
"SO"
"HBP"
"SH"
"SF"
"ROE"
"GDP"
"SB"
"CS"
"WPA"
"RE24"
"aLI"
"BOP"
"Pos"
"DK"
"FD"
"Home"
"BattingHand"
"PlayerGameNumber"
"L1BatterSO"
"L2BatterSO"
"L3BatterSO"
"L5BatterSO"
"L10BatterSO"
"L20BatterSO"
"L50BatterSO"
"L1BatterBB"
"L2BatterBB"
"L3BatterBB"
"L5BatterBB"
"L10BatterBB"
"L20BatterBB"
"L50BatterBB"
"L1BatterHR"
"L2BatterHR"
"L3BatterHR"
"L5BatterHR"
"L10BatterHR"
"L20BatterHR"
"L50BatterHR"
"L1BatterH"
"L2BatterH"
"L3BatterH"
"L5BatterH"
"L10BatterH"
"L20BatterH"
"L50BatterH"
"L1BatterR"
"L2BatterR"
"L3BatterR"
"L5BatterR"
"L10BatterR"
"L20BatterR"
"L50BatterR"
"L1BatterSB"
"L2BatterSB"
"L3BatterSB"
"L5BatterSB"
"L10BatterSB"
"L20BatterSB"
"L50BatterSB"
"L1BatterCS"
"L2BatterCS"
"L3BatterCS"
"L5BatterCS"
"L10BatterCS"
"L20BatterCS"
"L50BatterCS"
"OnTBD"
"AgainstTBD"
"PlayingInTBD"
"OnTEX"
"AgainstTEX"
"PlayingInTEX"
"OnANA"
"AgainstANA"
"PlayingInANA"
"OnSTL"
"AgainstSTL"
"PlayingInSTL"
"OnATL"
"AgainstATL"
"PlayingInATL"
"OnFLA"
"AgainstFLA"
"PlayingInFLA"
"OnHOU"
"AgainstHOU"
"PlayingInHOU"
"OnARI"
"AgainstARI"
"PlayingInARI"
"OnNYY"
"AgainstNYY"
"PlayingInNYY"
"OnBAL"
"AgainstBAL"
"PlayingInBAL"
"OnCHW"
"AgainstCHW"
"PlayingInCHW"
"OnDET"
"AgainstDET"
"PlayingInDET"
"OnCLE"
"AgainstCLE"
"PlayingInCLE"
"OnBOS"
"AgainstBOS"
"PlayingInBOS"
"OnSDP"
"AgainstSDP"
"PlayingInSDP"
"OnLAD"
"AgainstLAD"
"PlayingInLAD"
"OnCHC"
"AgainstCHC"
"PlayingInCHC"
"OnMIL"
"AgainstMIL"
"PlayingInMIL"
"OnKCR"
"AgainstKCR"
"PlayingInKCR"
"OnMIN"
"AgainstMIN"
"PlayingInMIN"
"OnNYM"
"AgainstNYM"
"PlayingInNYM"
"OnWSN"
"AgainstWSN"
"PlayingInWSN"
"OnPHI"
"AgainstPHI"
"PlayingInPHI"
"OnPIT"
"AgainstPIT"
"PlayingInPIT"
"OnCIN"
"AgainstCIN"
"PlayingInCIN"
"OnOAK"
"AgainstOAK"
"PlayingInOAK"
"OnSEA"
"AgainstSEA"
"PlayingInSEA"
"OnCOL"
"AgainstCOL"
"PlayingInCOL"
"OnSFG"
"AgainstSFG"
"PlayingInSFG"
"OnTOR"
"AgainstTOR"
"PlayingInTOR"
"HomeTeam"
"AirportCode"
"MaxTemp"
"MinTemp"
"MeanTemp"
"Prec"
"PrecEvent"
"BattingTeam"
"Unnamed: 0"
"AppDec"
"IP"
"ER"
"UER"
"Pit"
"Str"
"GSc"
"IR"
"IS"
"BF"
"PO"
"BK"
"WP"
"ERA"
"PitchingHand"
"L1PitcherSO"
"L2PitcherSO"
"L3PitcherSO"
"L5PitcherSO"
"L10PitcherSO"
"L20PitcherSO"
"L50PitcherSO"
"L1PitcherBB"
"L2PitcherBB"
"L3PitcherBB"
"L5PitcherBB"
"L10PitcherBB"
"L20PitcherBB"
"L50PitcherBB"
"L1PitcherHR"
"L2PitcherHR"
"L3PitcherHR"
"L5PitcherHR"
"L10PitcherHR"
"L20PitcherHR"
"L50PitcherHR"
"L1PitcherStr"
"L2PitcherStr"
"L3PitcherStr"
"L5PitcherStr"
"L10PitcherStr"
"L20PitcherStr"
"L50PitcherStr"
"L1PitcherSB"
"L2PitcherSB"
"L3PitcherSB"
"L5PitcherSB"
"L10PitcherSB"
"L20PitcherSB"
"L50PitcherSB"
"L1PitcherH"
"L2PitcherH"
"L3PitcherH"
"L5PitcherH"
"L10PitcherH"
"L20PitcherH"
"L50PitcherH"
"L1PitcherR"
"L2PitcherR"
"L3PitcherR"
"L5PitcherR"
"L10PitcherR"
"L20PitcherR"
"L50PitcherR"
"OpposingPitcher"
"PitAB"
"PitR"
"PitH"
"Pit2B"
"Pit3B"
"PitHR"
"PitBB"
"PitIBB"
"PitSO"
"PitHBP"
"PitSF"
"PitSH"
"PitSB"
"PitGDP"
"PitCS"
"PitWPA"
"PitRE24"
"PitaLI"
"PitDK"
"PitFD"
"PitcherPlayerGameNumber"
"Result"
"NumericDate"
'''

df = pd.read_csv('combined_batting_player.csv')

basic_columns = [
	"PitcherPlayerGameNumber",
	"NumericDate",
	"PitchingHand",
	"L1PitcherSO",
	"L2PitcherSO",
	"L3PitcherSO",
	"L5PitcherSO",
	"L10PitcherSO",
	"L20PitcherSO",
	"L50PitcherSO",
	"L1PitcherBB",
	"L2PitcherBB",
	"L3PitcherBB",
	"L5PitcherBB",
	"L10PitcherBB",
	"L20PitcherBB",
	"L50PitcherBB",
	"L1PitcherHR",
	"L2PitcherHR",
	"L3PitcherHR",
	"L5PitcherHR",
	"L10PitcherHR",
	"L20PitcherHR",
	"L50PitcherHR",
	"L1PitcherStr",
	"L2PitcherStr",
	"L3PitcherStr",
	"L5PitcherStr",
	"L10PitcherStr",
	"L20PitcherStr",
	"L50PitcherStr",
	"L1PitcherSB",
	"L2PitcherSB",
	"L3PitcherSB",
	"L5PitcherSB",
	"L10PitcherSB",
	"L20PitcherSB",
	"L50PitcherSB",
	"L1PitcherH",
	"L2PitcherH",
	"L3PitcherH",
	"L5PitcherH",
	"L10PitcherH",
	"L20PitcherH",
	"L50PitcherH",
	"L1PitcherR",
	"L2PitcherR",
	"L3PitcherR",
	"L5PitcherR",
	"L10PitcherR",
	"L20PitcherR",
	"L50PitcherR",
	"MaxTemp",
	"MinTemp",
	"MeanTemp",
	"BattingHand",
	"PlayerGameNumber",
	"L1BatterSO",
	"L2BatterSO",
	"L3BatterSO",
	"L5BatterSO",
	"L10BatterSO",
	"L20BatterSO",
	"L50BatterSO",
	"L1BatterBB",
	"L2BatterBB",
	"L3BatterBB",
	"L5BatterBB",
	"L10BatterBB",
	"L20BatterBB",
	"L50BatterBB",
	"L1BatterHR",
	"L2BatterHR",
	"L3BatterHR",
	"L5BatterHR",
	"L10BatterHR",
	"L20BatterHR",
	"L50BatterHR",
	"L1BatterH",
	"L2BatterH",
	"L3BatterH",
	"L5BatterH",
	"L10BatterH",
	"L20BatterH",
	"L50BatterH",
	"L1BatterR",
	"L2BatterR",
	"L3BatterR",
	"L5BatterR",
	"L10BatterR",
	"L20BatterR",
	"L50BatterR",
	"L1BatterSB",
	"L2BatterSB",
	"L3BatterSB",
	"L5BatterSB",
	"L10BatterSB",
	"L20BatterSB",
	"L50BatterSB",
	"L1BatterCS",
	"L2BatterCS",
	"L3BatterCS",
	"L5BatterCS",
	"L10BatterCS",
	"L20BatterCS",
	"L50BatterCS",
	"OnTBD",
	"AgainstTBD",
	"PlayingInTBD",
	"OnTEX",
	"AgainstTEX",
	"PlayingInTEX",
	"OnANA",
	"AgainstANA",
	"PlayingInANA",
	"OnSTL",
	"AgainstSTL",
	"PlayingInSTL",
	"OnATL",
	"AgainstATL",
	"PlayingInATL",
	"OnFLA",
	"AgainstFLA",
	"PlayingInFLA",
	"OnHOU",
	"AgainstHOU",
	"PlayingInHOU",
	"OnARI",
	"AgainstARI",
	"PlayingInARI",
	"OnNYY",
	"AgainstNYY",
	"PlayingInNYY",
	"OnBAL",
	"AgainstBAL",
	"PlayingInBAL",
	"OnCHW",
	"AgainstCHW",
	"PlayingInCHW",
	"OnDET",
	"AgainstDET",
	"PlayingInDET",
	"OnCLE",
	"AgainstCLE",
	"PlayingInCLE",
	"OnBOS",
	"AgainstBOS",
	"PlayingInBOS",
	"OnSDP",
	"AgainstSDP",
	"PlayingInSDP",
	"OnLAD",
	"AgainstLAD",
	"PlayingInLAD",
	"OnCHC",
	"AgainstCHC",
	"PlayingInCHC",
	"OnMIL",
	"AgainstMIL",
	"PlayingInMIL",
	"OnKCR",
	"AgainstKCR",
	"PlayingInKCR",
	"OnMIN",
	"AgainstMIN",
	"PlayingInMIN",
	"OnNYM",
	"AgainstNYM",
	"PlayingInNYM",
	"OnWSN",
	"AgainstWSN",
	"PlayingInWSN",
	"OnPHI",
	"AgainstPHI",
	"PlayingInPHI",
	"OnPIT",
	"AgainstPIT",
	"PlayingInPIT",
	"OnCIN",
	"AgainstCIN",
	"PlayingInCIN",
	"OnOAK",
	"AgainstOAK",
	"PlayingInOAK",
	"OnSEA",
	"AgainstSEA",
	"PlayingInSEA",
	"OnCOL",
	"AgainstCOL",
	"PlayingInCOL",
	"OnSFG",
	"AgainstSFG",
	"PlayingInSFG",
	"OnTOR",
	"AgainstTOR",
	"PlayingInTOR"
]

HR_columns = ['HR'] + basic_columns
Single_columns = ['1B'] + basic_columns
Double_columns = ['2B'] + basic_columns
Triple_columns = ['3B'] + basic_columns
RBI_columns = ['RBI'] + basic_columns
BB_columns = ['BB'] + basic_columns
SB_columns = ['SB'] + basic_columns
'''
build_xgboost_datasets(df, 'HR', 'HR', HR_columns)
build_xgboost_datasets(df, '1B', '1B', Single_columns)
build_xgboost_datasets(df, '2B', '2B', Double_columns)
build_xgboost_datasets(df, '3B', '3B', Triple_columns)
'''
build_xgboost_datasets(df, 'RBI', 'RBI', RBI_columns)
'''
build_xgboost_datasets(df, 'BB', 'BB', BB_columns)
build_xgboost_datasets(df, 'SB', 'SB', SB_columns)
'''






