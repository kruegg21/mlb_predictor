import urllib
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import datetime as dt

def get_page_data(url):
	#load HTML data from page into pagetext 
	page = urllib.urlopen(url)
	pagetext = page.read()

	# make some soup
	soup = BeautifulSoup(pagetext, 'html.parser')

	# column names
	col_names = ['LocalTime', 'TempF', 'DewPointF', 'Humidity', 'SeaLevelPressureIn',
				 'VisibilityMPH', 'WindDirection', 'WindSpeedMPH', 'GustSpeedMPH', 
				 'PrecipitationIn', 'Events', 'Conditions', 'WindDirDegrees', 'DateUTC']

	# create empty DataFrame
	df = pd.DataFrame(index = xrange(100), columns = col_names)

	# look through each page element
	row = 0
	for br in soup.findAll('br'):
	    next = br.nextSibling
	    if not (next and isinstance(next,NavigableString)):
	        continue
	    next2 = next.nextSibling
	    if next2 and isinstance(next2,Tag) and next2.name == 'br':
	        text = str(next).strip()
	        if text:
				col = 0
				for i in text.split(","):
					df.iat[row,col] = i
					col += 1
	    row += 1

	df = df[pd.notnull(df.LocalTime)]
	return df

# finds row in DataFrame with time closest to time in '%H:%M%p' format and returns
# the index of that row
def find_closest_time(df, time):
	# adds 1.5 hours to time to reflect middle of game
	mid = dt.datetime.strptime(time, "%I:%M%p") + dt.timedelta(hours = 1, minutes = 27)
	
	# find closest time
	time_column = df['LocalTime'].str.replace(" ", "")
	time_column = pd.to_datetime(time_column, format = "%I:%M%p")

	return (abs(time_column - mid)).idxmin()	

# gets weather data for all games in 'start_time_data_full.csv' file
if __name__ == "__main__":
	df = pd.read_csv('DataSets/RawData/StartTimeData/start_time_data_full.csv')
	# translate each team to airport code	
	airport_translation = {'TBA' : 'KTPA', 'OAK' : 'KOAK', 'NYA' : 'KLGA',
						   'KCA' : 'KMCI', 'BAL' : 'KBWI', 'TEX' : 'KGKY',
						   'CHN' : 'KORD', 'LAN' : 'KLAX', 'PHI' : 'KPHL',
						   'SDN' : 'KSAN', 'SLN' : 'KSTL', 'ANA' : 'KSNA',
	 					   'SEA' : 'KSEA', 'ATL' : 'KATL', 'COL' : 'KDEN',
	 					   'FLO' : 'KMIA', 'HOU' : 'KIAH', 'CHA' : 'KMDW',
	 					   'MIN' : 'KMSP', 'TOR' : 'KYYZ', 'ARI' : 'KPHX',
	 					   'SFN' : 'KSFO', 'BOS' : 'KBOS', 'CLE' : 'KCLE',
	 					   'DET' : 'KDTW', 'PIT' : 'KPIT', 'NYN' : 'KLGA',
	 					   'MON' : 'KYUL', 'MIL' : 'KMKE', 'CIN' : 'KCVG',
	 					   'WAS' : 'KDCA', 'MIA' : 'KMIA'}

	 # create empty DataFrame to hold weather data
	col_names = ['Team', 'Date', 'StartTime', 'LocalTime', 'TempF', 'DewPointF', 'Humidity', 'SeaLevelPressureIn',
	 			 'VisibilityMPH', 'WindDirection', 'WindSpeedMPH', 'GustSpeedMPH',
				 'PrecipitationIn', 'Events', 'Conditions', 'WindDirDegrees', 'DateUTC']
	weather_data = pd.DataFrame(index = range(len(df.index)), columns = col_names)

	for i in xrange(len(df.index)):
		airport = airport_translation[df.loc[i,'Team']]
		full_date = str(df.loc[i,'Date'])
		year = full_date[:4]
		month = full_date[4:6]
		if month[0] == '0':
			month = month[1]
		day = full_date[6:8]
		if day[0] == '0':
			day = day[1]
		start_time = df.loc[i,'StartTime']

		# create URL
		url = 'https://www.wunderground.com/history/airport/' + airport + '/' + str(year) + \
			  '/' + str(month) + '/' + str(day) + '/DailyHistory.html?format=1'

		# gather weather data for particular team and day
		day_weather = get_page_data(url)

		# get row index closest to middle of game
		row = find_closest_time(day_weather, df.loc[i,'StartTime'])

		# add in team, date, and start time data
		weather_data.iloc[i,0] = df.loc[i,'Team']
		weather_data.iloc[i,1] = str(int(df.loc[i,'Date']))
		weather_data.iloc[i,2] = df.loc[i,'StartTime']

		# parse weather data
		hourly_weather_data = day_weather.loc[row,:]
		for j in xrange(len(day_weather.columns)):
			weather_data.iloc[i,j+3] = hourly_weather_data.iloc[j]

		# dump
		weather_data_shrunk = weather_data[pd.notnull(weather_data.LocalTime)]
		weather_data_shrunk.to_csv('DataSets/RawData/WeatherData/weather_data_full.csv', index = False)


		