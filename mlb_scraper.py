import urllib
from bs4 import BeautifulSoup
import pandas as pd
import mechanize
import cookielib
# import concat_data as cd

# gets player data from one url from basketballreference.com, each page only show 100 entries of player data
def get_player_page_data(url, feature_names, browser):
	#load HTML data from page into pagetext 
	page = browser.visit(url)
	pagetext = browser.html

	# make some soup
	soup = BeautifulSoup(pagetext, 'html.parser')

	# create empty DataFrame object
	df = pd.DataFrame(columns = feature_names, index = range(0,1010))

	# scrape HTML tree
	row = 0
	for element in soup.find_all('tr'):
		column = 0;
		for subelement in element.find_all('td'):
			if(subelement.string is not None):
				if column == 1:
					# get player ID
					player_id_element = subelement.a
					df.iat[row,column] = player_id_element.get('href')[-15:-6]
					column += 1
				df.iat[row,column] = subelement.string
			column += 1
		row += 1

	return df

# scrapes new data from baseballreference.com starting at 
# current date and ending at year of 'starting_data'

# dumps to csv files in chunks divided by each team, home/away, year, and batting hand
# to get around 1500 row limit for baseballreference.com

def scrape_new_data(starting_year, ending_year, browser, only_pitching_data):
	######################################################################	
	# SCRAPE BATTING DATA
	# creates accumulator DataFrame to hold data (change feature names)
	feature_names = ['Rank','PlayerID','Player','Date','Team','Opp','Result','PA','AB','R','H',
					 '2B','3B','HR','RBI','BB','IBB','SO','HBP','SH','SF','ROE','GDP',
					 'SB','CS','WPA','RE24','aLI','BOP','Pos','DK','FD']
	team_list = ['TBD', 'TEX', 'ANA', 'STL', 'ATL', 'FLA','HOU', 'ARI', 'NYY', 
				 'BAL', 'CHW', 'DET', 'CLE', 'BOS', 'SDP', 'LAD','CHC', 'MIL', 
				 'KCR', 'MIN', 'NYM', 'WSN', 'PHI', 'PIT','CIN', 'OAK','SEA', 
				 'COL', 'SFG', 'TOR']
	home_away_list = ['H','V']
	batting_hand_list = ['R','L','B']
	year_list = range(starting_year, ending_year + 1)
	if not only_pitching_data:
		for team_id in team_list:
			for home_away in home_away_list:
				for year in year_list:
					for hand in batting_hand_list:
						print team_id + home_away + str(year) + "BATTING"
						starting_date = str(year) + "-01-01"
						accumulator = pd.DataFrame(columns = feature_names)
						i = 0
						reached_starting_date = 0
						while reached_starting_date == 0:
							offset = i * 300
							url = "http://www.baseball-reference.com/play-index/game_finder.cgi?gotresults&as=result_batter&offset=" + str(offset) + "&match=basic&suffix=&min_year_game=" + str(year-1) + "&max_year_game=" + str(year) + "&series=any&series_game=any&playoffs=&WL=any&game_length=any&team_id=" + team_id + "&team_lg=&opp_id=&opp_lg=&use_dh=&bats=" + hand + "&throws=&HV=" + home_away + "&game_site=&temperature_min=0&temperature_max=120&wind_speed_min=0&wind_speed_max=90&wind_direction_tolf=1&wind_direction_tocf=1&wind_direction_torf=1&wind_direction_fromlf=1&wind_direction_fromcf=1&wind_direction_fromrf=1&wind_direction_ltor=1&wind_direction_rtol=1&wind_direction_unknown=1&precipitation_unknown=1&precipitation_none=1&precipitation_drizzle=1&precipitation_showers=1&precipitation_rain=1&precipitation_snow=1&sky_unknown=1&sky_sunny=1&sky_cloudy=1&sky_overcast=1&sky_night=1&sky_dome=1&pos_1=1&pos_2=1&pos_3=1&pos_4=1&pos_5=1&pos_6=1&pos_7=1&pos_8=1&pos_9=1&pos_10=1&pos_11=1&pos_12=1&exactness=any&GS=anyGS&GF=anyGF&lineup_position=&number_matched=1&orderby=date_game&c1criteria=&c1gtlt=eq&c1val=0&c2criteria=&c2gtlt=eq&c2val=0&c3criteria=&c3gtlt=eq&c3val=0&c4criteria=&c4gtlt=eq&c4val=0&c5criteria=&c5gtlt=eq&c5val=1.0&c6criteria=&location=pob&locationMatch=is&pob=&pod=&pcanada=&pusa=&firstgames=&startgames=&lastgames=&firstteamgames=&startteamgames=&lastteamgames=&ajax=1&submitter=1&z=1&z=1&z=1&z=1&_=1456125400293"
							df = get_player_page_data(url, feature_names, browser)

							# data cleaning 
							df = df.drop([0,26,52,78,104,130,156,182,208,234,260,286])
							df = df.drop(df[pd.isnull(df.Date)].index)

							### NEW ####
							# reindex
							n = len(df.index)
							df.index = range(0,n)

							if n is not 0:
								# get date and turn starting date into numeric
								date = df.loc[n - 1].Date
								numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
									pd.to_datetime(pd.Series(starting_date))) / 86400000000000
								numeric_date = numeric_date.iloc[0]
								if (numeric_date < 0):
									reached_starting_date = 1
								else:
									i += 1

								if reached_starting_date:
									# remove all days past starting date from df
									for j in range(0,n):
										date = df.loc[j].Date
										numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
										pd.to_datetime(pd.Series(starting_date))) / 86400000000000
										numeric_date = numeric_date.iloc[0]
										if (numeric_date < 0):
											df = df.drop(j)

								### END NEW #### 
								accumulator = pd.concat([accumulator,df])
								accumulator.to_csv('DataSets/RawData/Batting/' + team_id + '_vs_' + home_away + '_' + str(year) + '_Batting_' + hand + '_new.csv', index = False)
							else:
								reached_starting_date = 1
								accumulator.to_csv('DataSets/RawData/Batting/' + team_id + '_vs_' + home_away + '_' + str(year) + '_Batting_' + hand + '_new.csv', index = False)
	######################################################################

	######################################################################
	# SCRAPE PITCHING DATA
	# dumps into chunks separated by team, year, and pitching hand

	feature_names = ['Rank','PlayerID','Player','Date','Team','Opp','Result','AppDec','IP','H','R','ER',
					 'BB','SO','HR','UER','Pit','Str','GSc','IR','IS','BF','AB','2B','3B','IBB',
					 'HBP','SH','SF','GDP','SB','CS','PO','BK','WP','ERA','WPA','RE24','aLI','DK','FD']
	pitching_hand_list = ['R','L']
	for team_id in team_list:
		for year in year_list:
			for hand in pitching_hand_list:
				print team_id + str(year) + "PITCHING"
				starting_date = str(year) + "-01-01"
				accumulator = pd.DataFrame(columns = feature_names)
				i = 0
				reached_starting_date = 0
				while reached_starting_date == 0:
					offset = i * 300
					url = "http://www.baseball-reference.com/play-index/game_finder.cgi?gotresults&as=result_pitcher&offset=" + str(offset) + "&match=basic&suffix=&min_year_game=" + str(year-1) + "&max_year_game=" + str(year) + "&series=any&series_game=any&playoffs=&WL=any&game_length=any&team_id=" + team_id + "&team_lg=&opp_id=&opp_lg=&use_dh=&bats=any&throws=" + hand + "&HV=&game_site=&temperature_min=0&temperature_max=120&wind_speed_min=0&wind_speed_max=90&wind_direction_tolf=1&wind_direction_tocf=1&wind_direction_torf=1&wind_direction_fromlf=1&wind_direction_fromcf=1&wind_direction_fromrf=1&wind_direction_ltor=1&wind_direction_rtol=1&wind_direction_unknown=1&precipitation_unknown=1&precipitation_none=1&precipitation_drizzle=1&precipitation_showers=1&precipitation_rain=1&precipitation_snow=1&sky_unknown=1&sky_sunny=1&sky_cloudy=1&sky_overcast=1&sky_night=1&sky_dome=1&pos_1=1&pos_2=1&pos_3=1&pos_4=1&pos_5=1&pos_6=1&pos_7=1&pos_8=1&pos_9=1&pos_10=1&pos_11=1&pos_12=1&exactness=any&GS=anyGS&GF=anyGF&lineup_position=&number_matched=1&orderby=date_game&c1criteria=&c1gtlt=eq&c1val=0&c2criteria=&c2gtlt=eq&c2val=0&c3criteria=&c3gtlt=eq&c3val=0&c4criteria=&c4gtlt=eq&c4val=0&c5criteria=&c5gtlt=eq&c5val=1.0&c6criteria=&location=pob&locationMatch=is&pob=&pod=&pcanada=&pusa=&firstgames=&startgames=&lastgames=&firstteamgames=&startteamgames=&lastteamgames=&ajax=1&submitter=1&z=1&z=1&z=1&z=1&_=1456125400293"
					df = get_player_page_data(url, feature_names, browser)

					# data cleaning 
					df = df.drop([0,26,52,78,104,130,156,182,208,234,260,286])
					df = df.drop(df[pd.isnull(df.Date)].index)

					### NEW ####
					# reindex
					n = len(df.index)
					df.index = range(0,n)

					# get date and turn starting date into numeric
					date = df.loc[n - 1].Date
					numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
						pd.to_datetime(pd.Series(starting_date))) / 86400000000000
					numeric_date = numeric_date.iloc[0]
					if (numeric_date < 0):
						reached_starting_date = 1
					else:
						i += 1

					if reached_starting_date:
						# remove all days past starting date from df
						for j in range(0,n):
							date = df.loc[j].Date
							numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
							pd.to_datetime(pd.Series(starting_date))) / 86400000000000
							numeric_date = numeric_date.iloc[0]
							if (numeric_date < 0):
								df = df.drop(j)

					### END NEW #### 
					accumulator = pd.concat([accumulator,df])
					accumulator.to_csv('DataSets/RawData/Pitching/' + team_id + '_vs_' + str(year) + '_Pitching_' + hand + '_new.csv', index = False)
	######################################################################

# gets data on the start time of games from sportsdatabase.com
# this website only has start time data going back to the 2004 season
def get_start_time_data(browser):
	# hard coded URL
	url = 'http://b2b.sportsdatabase.com/mlb/query?output=default&su=1&ou=1&sdql=date%2Cteam%2Co%3Astart+time%40scored+first%3D1&submit=++S+D+Q+L+%21++'
	
	#load HTML data from page into pagetext 
	page = browser.visit(url)
	pagetext = browser.html

	# make some soup
	soup = BeautifulSoup(pagetext, 'html.parser')

	# make empty dataframe
	df = pd.DataFrame(columns = ['Date','Team','StartTime'], index = xrange(len(soup.find_all('tr'))))

	row = 0
	for element in soup.find_all('tr'):
		subelements = element.find_all('td')
		if len(subelements) == 3:
			if subelements[0].string is not None:
				df.iat[row, 0] = subelements[0].string.lstrip('\n').rstrip('\n')
				df.iat[row, 1] = subelements[1].string.lstrip('\n').rstrip('\n')
				df.iat[row, 2] = subelements[2].string.lstrip('\n').rstrip('\n')
				row += 1

	df = df[pd.notnull(df.Date)]

	df['Date'].map(lambda x: x.lstrip('\n').rstrip('\n'))
	df['Team'].map(lambda x: x.lstrip('\n').rstrip('\n'))
	df['StartTime'].map(lambda x: x.lstrip('\n').rstrip('\n'))

	df.to_csv('testtest.csv')

# downloadas regular season batting order from baseballreference.com
def get_batting_order_data(starting_year, ending_year):
	team_list = ['TBD', 'TEX', 'ANA', 'STL', 'ATL', 'FLA','HOU', 'ARI', 'NYY', 
			 'BAL', 'CHW', 'DET', 'CLE', 'BOS', 'SDP', 'LAD','CHC', 'MIL', 
			 'KCR', 'MIN', 'NYM', 'WSN', 'PHI', 'PIT','CIN', 'OAK','SEA', 
			 'COL', 'SFG', 'TOR']
	year_list = xrange(starting_year, ending_year + 1)

	# create empty DataFrame
	batting_order_data = pd.DataFrame()

	# iterate through all teams and years gathering batting order data
	for team in team_list:
		for year in year_list:
			print team, year
			# create empty DataFrame
			col_names = ['Team','Date','B1','B2','B3','B4','B5','B6','B7','B8','B9']
			df = pd.DataFrame(columns = col_names, index = range(200))

			# make URL
			url = 'http://www.baseball-reference.com/teams/' + team + \
				  '/' + str(year) + '-batting-orders.shtml'

			#load HTML data from page into pagetext 
			page = urllib.urlopen(url)
			pagetext = page.read()

			# make some soup
			soup = BeautifulSoup(pagetext, 'html.parser')
			row = 0
			for element in soup.find_all('tr'):
				subelements = element.find_all('a')

				# check to make sure we are only gathering data
				# from parts of the page with batting order information
				if len(subelements) is 12:
					# set team as first column
					df.iat[row,0] = team

					# get date as second column
					df.iat[row,1] = subelements[1]['href'][-15:-7]

					# fill in batting order for remaining columns
					column = 2
					for subelement in subelements:
						if subelement.get('data-entry-id') is not None:
							df.iat[row,column] = subelement.get('data-entry-id')
							column += 1
					row += 1

			# remove empty rows
			df = df[pd.notnull(df.Team)]

			# add newly scraped data to full set
			batting_order_data = pd.concat([batting_order_data, df])

			# dump
			batting_order_data.to_csv('DataSets/RawData/BattingOrder/' + team + str(year) + 'Batting_Order.csv' , index = False)

# gets schedules for each team from baseball-almanac.com
def get_team_schedules(starting_year, ending_year):
	team_list = ['TBR', 'TBA', 'OAK', 'NYA', 'KCA', 'BAL', 'TEX',
				 'CHN', 'LAN', 'PHI', 'SDN', 'SLN', 'ANA', 'SEA', 
				 'ATL', 'COL', 'FLO', 'HOU', 'CHA', 'MIN', 'MIL', 
				 'TOR', 'ARI', 'SFN', 'BOS', 'CLE', 'DET', 'PIT', 
				 'CIN', 'NYN', 'WAS', 'MON', 'MIA', 'ANG', 'HOA', 
				 'ML4', 'CN5', 'WS0'] 
	year_list = xrange(starting_year, ending_year + 1)

	# translates team names from baseball-almanac.com to the team names
	# in baseballreference.com
	team_translation_list = {'TBR' : 'TBA', 'TBA' : 'TBA', 'OAK' : 'OAK',
							 'NYA' : 'NYA', 'KCA' : 'KCA', 'BAL' : 'BAL',
							 'TEX' : 'TEX', 'CHN' : 'CHN', 'LAN' : 'LAN',
							 'PHI' : 'PHI', 'SDN' : 'SDN', 'SLN' : 'SLN',
							 'ANA' : 'ANA', 'SEA' : 'SEA', 'ATL' : 'ATL',
							 'COL' : 'COL', 'FLO' : 'FLO', 'HOU' : 'HOU',
							 'CHA' : 'CHA', 'MIN' : 'MIN', 'MIL' : 'MIL',
							 'TOR' : 'TOR', 'ARI' : 'ARI', 'SFN' : 'SFN',
							 'BOS' : 'BOS', 'CLE' : 'CLE', 'DET' : 'DET',
							 'PIT' : 'PIT', 'CIN' : 'CIN', 'NYN' : 'NYN',
							 'WAS' : 'WAS', 'MON' : 'MON', 'MIA' : 'MIA',
							 'ANG' : 'ANA', 'HOA' : 'HOU', 'ML4' : 'MIL',
							 'CN5' : 'CIN', 'WS0' : 'WAS'}

	# create empty DataFrame
	df = pd.DataFrame(columns = ['Date', 'Team', 'DoubleHeader'], index = xrange(162 * 30 * 30))
	row = 0

	for team in team_list:
		for year in year_list:
			# create URL
			url = 'http://www.baseball-almanac.com/teamstats/schedule.php?y=' + str(year) + '&t=' + team

			#load HTML data from page into pagetext 
			page = urllib.urlopen(url)
			pagetext = page.read()

			# make some soup
			soup = BeautifulSoup(pagetext, 'html.parser')

			print team, year

			games = 0
			if len(soup.find_all('td', {"class" : "datacolBoxC"})) > 2:
				for element in soup.find_all('tr'):
					subelements = element.find_all('td', {"class" : "datacolBoxC"})
					oppenent = element.find_all('td', {"class" : "datacolBox"})
					if (len(subelements) > 1) & (len(subelements) < 20):
						if (oppenent[0].string[0] == 'v'):
							df.iat[row,0] = subelements[1].string
							df.iat[row,1] = team_translation_list[team]
							if subelements[0].string[-1] == 'I':
								df.iat[row,2] = 1
							else:
								df.iat[row,2] = 0
							row += 1
							games += 1
			print games
			print '\n'
		df.to_csv('DataSets/RawData/TeamSchedules/team_schedules.csv', index = False)				
	df = df[pd.notnull(df.Team)]
	df.to_csv('DataSets/RawData/TeamSchedules/team_schedules.csv', index = False)	
	print len(df.index)

# get the start time data for all games in 'team_schedules.csv' file
def get_start_time_data():
	# all the team IDs from baseballreference.com
	team_list = ['TBA', 'OAK', 'NYA', 'KCA', 'BAL', 'TEX',
				 'CHN', 'LAN', 'PHI', 'SDN', 'SLN', 'ANA',
				 'SEA', 'ATL', 'COL', 'FLO', 'HOU', 'CHA',
				 'MIN', 'MIL', 'TOR', 'ARI', 'SFN', 'BOS',
				 'CLE', 'DET', 'PIT', 'CIN', 'NYN', 'WAS', 'MON'] 	   
	
	# read 'team_schedules.csv' file
	team_schedules = pd.read_csv('team_schedules.csv')

	team_schedules = team_schedules.iloc[24944:25277,:]
	team_schedules.index = xrange(len(team_schedules.index))
	print team_schedules


	# create empty DataFrame
	col_names = ['Team', 'Date', 'StartTime', 'FieldName']
	df = pd.DataFrame(columns = col_names, index = xrange(len(team_schedules.index)))

	# periodically save every number of rows in case of internet timeout
	periodic_save_counter = 0
	row = 0
	for i in team_schedules.index:
		date = team_schedules.iat[i,0]
		team = team_schedules.iat[i,1]
		double_header = team_schedules.iat[i,2]

		date = str(date)[-4:] + str(date)[:2] + str(date)[3:5]
		url = 'http://www.baseball-reference.com/boxes/' + team + '/' + \
			   team + date + str(int(double_header)) + '.shtml'

		print url
		#load HTML data from page into pagetext 
		page = urllib.urlopen(url)
		pagetext = page.read()

		# make some soup
		soup = BeautifulSoup(pagetext, 'html.parser')

		elements = soup.findAll("div", { "class" : "bold_text float_left"})
		if len(elements) is not 0:
			df.iat[row,0] = team
			df.iat[row,1] = date
			df.iat[row,2] = elements[0].string[-7:].lstrip()

			# if there is no information available for stadium, make 'FieldName' unknown
			if elements[1].string is not None:
				df.iat[row,3] = elements[1].string[2:]
				print elements[0].string[-7:].lstrip()
				print elements[1].string[2:]
			else:
				df.iat[row,3] = 'Unknown'
				print elements[0].string[-7:].lstrip()
				print 'Unknown'
			row += 1
			periodic_save_counter += 1

		if periodic_save_counter > 200:
			print "SAVED AT ROW:"
			print row
			df.to_csv('start_time_data5.csv', index = False)
			periodic_save_counter = 0
	df.to_csv('start_time_data5.csv', index = False)

	'''
	start_time_data = pd.DataFrame()
	for team in team_list:
		for year in year_list:
			# after every year, concat with large DataFrame
			col_names = ['Team', 'Date', 'StartTime', 'FieldName']
			df = pd.DataFrame(columns = col_names, index = xrange(200))
			row = 0
			for month in month_list:
				if month < 10:
					month = '0' + str(month)
				else:
					month = str(month)
				for day in day_list:
					for double_header in [0,1,2]:
						if day < 10:
							day = '0' + str(day)
						else:
							day = str(day)
						print team, year, month, day
						# build URL
						url = 'http://www.baseball-reference.com/boxes/' + team + '/' + \
							   team + str(year) + month + day + str(double_header) + '.shtml'	

						#load HTML data from page into pagetext 
						page = urllib.urlopen(url)
						pagetext = page.read()

						# make some soup
						soup = BeautifulSoup(pagetext, 'html.parser')

						elements = soup.findAll("div", { "class" : "bold_text float_left"})
						if len(elements) is not 0:
							df.iat[row,0] = team
							df.iat[row,1] = str(year) + month + day
							df.iat[row,2] = elements[0].string[-7:].lstrip()
							df.iat[row,3] = elements[1].string[2:]
							print elements[0].string[-7:].lstrip()
							print elements[1].string[2:]
							row += 1
			df = df[pd.notnull(df.Team)]
			start_time_data = pd.concat([start_time_data, df])
			start_time_data.to_csv('testtesttes.csv', index = False)
	'''

def get_team_data(starting_year, ending_year, browser):
	team_list = ['TBD', 'TEX', 'ANA', 'STL', 'ATL', 'FLA','HOU', 'ARI', 'NYY', 
			 'BAL', 'CHW', 'DET', 'CLE', 'BOS', 'SDP', 'LAD','CHC', 'MIL', 
			 'KCR', 'MIN', 'NYM', 'WSN', 'PHI', 'PIT','CIN', 'OAK','SEA', 
			 'COL', 'SFG', 'TOR']
	year_list = xrange(starting_year, ending_year)

	for team in team_list:
		for year in year_list:
			starting_date = str(year) + "-01-01"
			accumulator = pd.DataFrame(columns = feature_names)

			# create URL
			url = 'http://www.baseball-reference.com/play-index/game_finder.cgi?class=team&type=b#gotresults&as=team_batting&offset=0&match=basic&suffix=&min_year_game=' + str(year) + '&max_year_game=' + str(year) + '&series=any&series_game=any&playoffs=&WL=any&game_length=any&team_id=' + team + '&team_lg=&opp_id=&opp_lg=&use_dh=&HV=any&game_site=&temperature_min=0&temperature_max=120&wind_speed_min=0&wind_speed_max=90&wind_direction_tolf=1&wind_direction_tocf=1&wind_direction_torf=1&wind_direction_fromlf=1&wind_direction_fromcf=1&wind_direction_fromrf=1&wind_direction_ltor=1&wind_direction_rtol=1&wind_direction_unknown=1&precipitation_unknown=1&precipitation_none=1&precipitation_drizzle=1&precipitation_showers=1&precipitation_rain=1&precipitation_snow=1&sky_unknown=1&sky_sunny=1&sky_cloudy=1&sky_overcast=1&sky_night=1&sky_dome=1&number_matched=1&orderby=HR&c1criteria=&c1gtlt=eq&c1val=0&c2criteria=&c2gtlt=eq&c2val=0&c3criteria=&c3gtlt=eq&c3val=0&c4criteria=&c4gtlt=eq&c4val=0&c5criteria=&c5gtlt=eq&c5val=1.0&c6criteria=&firstteamgames=&startteamgames=&lastteamgames=&ajax=1&submitter=1'

			# data cleaning 
			df = df.drop([0,26,52,78,104,130,156,182,208,234,260,286])
			df = df.drop(df[pd.isnull(df.Date)].index)

			### NEW ####
			# reindex
			n = len(df.index)
			df.index = range(0,n)

			if n is not 0:
				# get date and turn starting date into numeric
				date = df.loc[n - 1].Date
				numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
					pd.to_datetime(pd.Series(starting_date))) / 86400000000000
				numeric_date = numeric_date.iloc[0]
				if (numeric_date < 0):
					reached_starting_date = 1
				else:
					i += 1

				if reached_starting_date:
					# remove all days past starting date from df
					for j in range(0,n):
						date = df.loc[j].Date
						numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
						pd.to_datetime(pd.Series(starting_date))) / 86400000000000
						numeric_date = numeric_date.iloc[0]
						if (numeric_date < 0):
							df = df.drop(j)

				### END NEW #### 
				accumulator = pd.concat([accumulator,df])
				accumulator.to_csv('DataSets/RawData/' + team_id + '_vs_' + home_away + '_' + str(year) + '_Batting_' + hand + '_new.csv', index = False)
			else:
				reached_starting_date = 1
				accumulator.to_csv('DataSets/RawData/' + team_id + '_vs_' + home_away + '_' + str(year) + '_Batting_' + hand + '_new.csv', index = False)

if __name__ == "__main__":
	# USE CHROME BROWSER FOR FACEBOOK LOGIN FOR BASEBALLREFERENCE.COM
	from splinter import Browser
	browser= Browser('chrome')

	user_email = raw_input("enter users email address ")
	user_pass = raw_input("enter users password ")
	browser.visit('http://www.facebook.com')

	browser.fill('email', user_email)
	browser.fill('pass', user_pass)

	#Here is what I made a slight change
	button = browser.find_by_id('loginbutton')
	button.click()

	#I didn't find the page saving function for facebook using Splinter but as an alternative I found screenshot feature. 

	# The site we will navigate into, handling it's session
	browser.visit('http://www.baseball-reference.com/my/auth.cgi?return_to=http://www.baseball-reference.com/')
	browser.click_link_by_href('/my/auth.cgi?do=oauth_login&service=facebook&return_to=')
	# print response.read()
	# scrape_new_data(starting_year, ending_year, browser, only_pitching_data)
	scrape_new_data(2010, 2015, browser, 1)
	'''

	get_start_time_data()




	def convert_excel_date_format(file_name, date_column):
		df = pd.read_csv(file_name, parse_dates = [date_column])
		df.to_csv(file_name, date_format= '%m-%d-%Y', index = False)

	convert_excel_date_format('team_schedules.csv', 0)

	'''

	'''
	df1 = pd.read_csv('start_time_data.csv')
	df2 = pd.read_csv('start_time_data2.csv')
	df3 = pd.read_csv('start_time_data3.csv')
	df4 = pd.read_csv('start_time_data4.csv')
	df5 = pd.read_csv('start_time_data5.csv')

	df1 = df1[pd.notnull(df1.Team)]
	df2 = df2[pd.notnull(df2.Team)]
	df3 = df3[pd.notnull(df3.Team)]
	df4 = df4[pd.notnull(df4.Team)]
	df5 = df5[pd.notnull(df5.Team)]

	print len(df1.index)
	print len(df2.index)
	print len(df3.index)
	print len(df4.index)
	print len(df5.index)

	df = pd.concat([df1, df2, df3, df4, df5])

	for i in df['Team'].unique():
		print i
		print len(df[df['Team'] == i])
		print '\n'

	print len(df.index)

	df.to_csv('start_time_data_full.csv')
	'''


	'''
	get_team_schedules(2004, 2015)

	'''