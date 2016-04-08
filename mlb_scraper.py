import urllib
from bs4 import BeautifulSoup
import pandas as pd
import mechanize
import cookielib
# import concat_data as cd

# gets player data from one url from basketballreference.com, each page only show 100 entries of player data
def get_page_data(url, feature_names, browser):
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
				print subelement.string
				df.iat[row,column] = subelement.string
			column += 1
		row += 1

	return df

# scrapes new data from baseballreference.com starting at 
# current date and ending at year of 'starting_data'

# dumps to csv files in chunks divided by each team, opponent divsion, and year
# to get around 1500 row limit for baseballreference

def scrape_new_data(starting_year, ending_year, browser):
	# creates accumulator DataFrame to hold data (change feature names)
	feature_names = ['Rank','Player','Date','Team','Opp','Result','PA','AB','R','H',
					 '2B','3B','HR','RBI','BB','IBB','SO','HBP','SH','SF','ROE','GDP',
					 'SB','CS','WPA','RE24','aLI','BOP','Pos','DK','FD']

	# SCRAPE BATTING DATA
	team_list = ['TBD', 'TEX', 'ANA', 'STL', 'ATL', 'FLA','HOU', 'ARI', 'NYY', 
				 'BAL', 'CHW', 'DET', 'CLE', 'BOS', 'SDP', 'LAD','CHC', 'MIL', 
				 'KCR', 'MIN', 'NYM', 'WSN', 'PHI', 'PIT','CIN', 'OAK','SEA', 
				 'COL', 'SFG', 'TOR']
	home_away_list = ['H','V']
	batting_hand_list = ['R','L','B']
	pitching_hand_list = ['R','L']
	year_list = range(starting_year, ending_year + 1)

	'''
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
						df = get_page_data(url, feature_names, browser)

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
							accumulator.to_csv(team_id + '_vs_' + home_away + '_' + str(year) + '_B_' + hand + '_new.csv', index = False)
						else:
							reached_starting_date = 1
							accumulator.to_csv(team_id + '_vs_' + home_away + '_' + str(year) + '_B_' + hand + '_new.csv', index = False)
	'''

	feature_names = ['Rank','Player','Date','Team','Opp','Result','AppDec','IP','H','R','ER',
					 'BB','SO','HR','UER','Pit','Str','GSc','IR','IS','BF','AB','2B','3B','IBB',
					 'HBP','SH','SF','GDP','SB','CS','PO','BK','WP','ERA','WPA','RE24','aLI','DK','FD']
	# SCRAPE PITCHING DATA
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
					df = get_page_data(url, feature_names, browser)

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
					accumulator.to_csv(team_id + '_vs_' + str(year) + '_P_' + hand + '_new.csv', index = False)


from splinter import Browser

user_email = raw_input("enter users email address ")
user_pass = raw_input("enter users password ")
browser= Browser('chrome')
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
scrape_new_data(2010, 2015, browser)

