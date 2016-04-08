import pandas as pd
import numpy as np

def error_checking(df, string_indicator, verbose):
	print string_indicator + ':'

	print "ROWS:"
	print df.index

	print "NUM ROW:"
	print len(df.index)

	if verbose:
		for column in df.columns:
			ser = df.loc[:,column]
			print column + ' ' + str(sum(ser.isnull())) + ' ' + str(sum(ser == -999)) + ' ' + str(sum(ser < 0))
	else:
		df.info()

	# sum of prediction 
	if "Pred" in df.columns:
		print "Sum of Pred"
		print df.loc[:,"Pred"].sum()
	else:
		print "Pred not in columns"

	# sum of new
	if "New" in df.columns:
		print "Sum of New"
		print df.loc[:,"New"].sum()
	else:
		print "New not in columns"

	print "\n\n"

def get_averages(data_frame, column, mid_column_name, sorted_column):
	day_list = [1,2,3,5,10,20,50]

	print "GETTING AVERAGES FOR"
	print column
	# MUST GROUP BY PLAYER TO GET ACCURATE AVERAGES
	for i in day_list:
		# get stat column
		col = data_frame.loc[:,column]

		# get rolling mean (includes the day of stat, so this
		# must be shifted to create the correct window)
		col = pd.rolling_mean(col, i)
		# shift rolling mean
		col.fillna(-999, inplace = True)
		col = pd.Series(col.iloc[:-1])
		col = pd.Series(-999).append(col)
		col.index = xrange(len(col.index))

		# check for spill over
		col[data_frame.loc[:,sorted_column] <= i] = -999

		# reindex to remedy index change made during shift
		col.index = xrange(len(col.index))
		# add to data frame
		data_frame["L" + str(i) + mid_column_name + column] = col

	return data_frame

def add_numeric_date(df):
	n = len(df.index)
	df.index = xrange(n)

	# DROP NUMERIC DATE IF IT IS ALREADY IN COLUMNS
	if 'NumericDate' in df.columns:
		df.drop('NumericDate', 1, inplace = True)

	date_start = np.repeat("2000-01-01", n)
	date_start = pd.Series(data = date_start)
	numeric_date = pd.to_numeric(pd.to_datetime(df.loc[:,"Date"]) - \
		pd.to_datetime(pd.Series(date_start))) / 86400000000000
	df["NumericDate"] = numeric_date
	return df

# calculates the 'game_number' for each row in dataframe. The 
# game number is the number of games a particular game is past
# the first row chronologically in the dataframe. The 'sort_column'
# specifies the column we are finding the game number for. For example,
# if we are looking for each player's game number, we use 'Player' as 
# the 'sort_column' argument

def calculate_game_number(df, sort_column):
	n = len(df.index)

	df = df.sort_values(by = [sort_column,"Date"])
	df.index = range(0,n)

	game_number_list = [0] * n
	game_number = 1
	currently_on = df.loc[0,sort_column]
	for i in range(0,n):
		if df.loc[i,sort_column] == currently_on:
			game_number_list[i] = game_number
			game_number += 1
		else:
			currently_on = df.loc[i,sort_column]
			game_number_list[i] = 1
			game_number = 2
	new_column_name = sort_column + "GameNumber"
	df[new_column_name] = game_number_list

	return df  