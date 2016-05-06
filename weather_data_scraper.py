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
	        print text
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

if __name__ == "__main__":
	df = pd.read_csv('DataSets/RawData/StartTimeData/start_time_data_full.csv')
	# translate each team to airport code	
	airport_translation = {'TBA' : 'KTPA', 'OAK' : 'KOAK', 'NYA' : 'KLGA',
						   'KCA' : 'KMCI', 'BAL' : 'KBWI', 'TEX' : 'KGKY',
						   'CHN' : 'KSFO', 'LAN' : 'KSFO', 'PHI' : 'KSFO',
						   'SDN' : 'KSFO', 'SLN' : 'KSFO', 'ANA' : 'KSFO',
	 					   'SEA' : 'KSFO', 'ATL' : 'KSFO', 'COL' : 'KSFO',
	 					   'FLO' : 'KSFO', 'HOU' : 'KSFO', 'CHA' : 'KSFO',
	 					   'MIN' : 'KSFO', 'TOR' : 'KSFO', 'ARI' : 'KSFO',
	 					   'SFN' : 'KSFO', 'BOS' : 'KSFO', 'CLE' : 'KSFO',
	 					   'DET' : 'KSFO', 'PIT' : 'KSFO', 'NYN' : 'KSFO',
	 					   'MON' : 'KSFO', 'MIL' : 'KSFO', 'CIN' : 'KSFO',
	 					   'WAS' : 'KSFO', 'MIA' : 'KSFO'}

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
		print airport, year, month, day, start_time

		# create URL
		url = 'https://www.wunderground.com/history/airport/' + airport + '/' + str(year) + \
			  '/' str(month) + '/' + str(day) + '/DailyHistory.html?format=1'
		get_page_data(url)
		