import pandas as pd

# combines umpire, date, and weather data
def combine_game_stats():
	start_time_data = pd.read_csv('DataSets/RawData/StartTimeData/start_time_data.csv')
	weather_data = pd.read_csv('DataSets/RawData/WeatherData/weather_data_full.csv')
	batting_order_data = pd.read_csv('DataSets/RawData/BattingOrder/batting_order.csv')

	print "NUMBER OF START TIME ROWS"
	print len(start_time_data.index)
	print "NUMBER OF WEATHER ROWS"
	print len(weather_data.index)

	df = pd.merge(start_time_data, weather_data, on = ['Team', 'Date', 'StartTime'], how = 'outer')

	df_missing_start_time = df[pd.isnull(df.FieldName)]
	df_missing_start_time.to_csv('missing_start_time.csv', index = False)

	df_missing_weather = df[pd.isnull(df.TempF)]
	df_missing_weather.to_csv('missing_weather.csv', index = False)
	print len(df.index)

	df.to_csv('full_set.csv', index = False)


# combines the pieces of the scraped chunks of batting and pitching data 
# and dumps them to 'full_batting_dataset.csv' and 'full_pitching_dataset.csv'
def build_from_scratch(start_year):
	# combine chunks of batting datasets
	df = pd.DataFrame()
	team_list = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN',
                 'CLE', 'COL', 'DET', 'FLA', 'HOU', 'KCR', 'LAD', 'MIL',
                 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA',
                 'SFG', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']
	home_away_list = ['H','V']
	pitching_hand_list = ['R','L']
	batting_hand_list = ['R','L','B']
	for year in range(start_year, 2016):
		for team in team_list:
			for hv in home_away_list:
				for hand in batting_hand_list:
					new_frame = pd.read_csv(team + '_vs_' + hv + '_' + str(year) + '_B_' + hand + '_new.csv')
					if hv == 'H':
						new_frame["Home"] = 1
					else:
						new_frame["Home"] = 0

					if hand == 'R':
						new_frame["BattingHand"] = 1
					elif hand == 'B':
						new_frame["BattingHand"] = 2
					else:
						new_frame["BattingHand"] = 0

					df = pd.concat([df, new_frame])
	df.to_csv('full_batting_dataset.csv', index = False)

	# combine chunks of pitching datasets
	df = pd.DataFrame()
	for year in range(start_year, 2016):
		for team in team_list:
			for hand in pitching_hand_list:
				new_frame = pd.read_csv(team + '_vs_' + str(year) + '_P_' + hand + '_new.csv')

				if hand == 'R':
					new_frame["PitchingHand"] = 1
				else:
					new_frame["PitchingHand"] = 0

				df = pd.concat([df, new_frame])
	df.to_csv('full_pitching_dataset.csv', index = False)

if __name__ == '__main__':
	combine_game_stats()