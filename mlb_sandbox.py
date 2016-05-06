import openweather
import pandas as pd
from datetime import datetime
import pyowm
import numpy as np

df = pd.read_csv('testtest.csv')

df['ParsedDate'] = pd.to_datetime(df.Date, format = "%Y%m%d")

df.StartTime.mod(100)
df.StartTime.div(100).apply(np.floor)

'''
import rpy2.robjects as robjects
# R package names
packnames = ('weatherData')

# import rpy2's package module
import rpy2.robjects.packages as rpackages

if rpackages.isinstalled('weatherData'):
	have_tutorial_packages = True
else:
	have_tutorial_packages = False

if not have_tutorial_packages:
    # import R's utility package
    utils = rpackages.importr('weatherData')
    # select a mirror for R packages
    utils.chooseCRANmirror(ind=1) # select the first mirror in the list

if not have_tutorial_packages:
    # R vector of strings
    from rpy2.robjects.vectors import StrVector
    # file
    packnames_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
    if len(packnames_to_install) > 0:
        utils.install_packages(StrVector(packnames_to_install))

print 'here'
'''

'''
df = pd.read_csv('combined_batting_player_test.csv')

df["Datetime"] = pd.to_datetime(df.Date)

print df.Datetime
'''

'''
ow = openweather.OpenWeather()

# find weather stations near me
stations = ow.find_stations_near(
     -65.3283,
     40.1803, 
     10000000000  # kilometer radius
)

# dictionary to link teams to airport codes
# CLE -> Cleveland Hopkins KCLE
# ARI -> Phoenix Sky Harbor KPHX
# LAD -> Burbank Airpot KBUR
# BAL -> Baltimore Washington KBWI
# CHC -> Midway KMDW
# STL -> Lambert KSTL
# ATL -> Hartsfield-Jackson KATL
# WSN -> Washington Dulles KIAD
# HOU -> George Bush KIAH
# CIN -> Cincinatti Northern Kentucky KCVG
# KCR -> Kansas City KMCI
# DET -> Detroit KDTW
# PHI -> Philadelphia KPHL
# SFG -> SFO KSFO
# MIL -> General Mitchell KMKE
# MIA -> Miami KMIA
# SDP -> San Diego KSAN
# SEA -> Seattle Tacoma KSEA
# NYM -> LaGuardia KLGA
# COL -> Denver KDEN
# LAA -> John Wayne KSNA
# PIT -> Pittsbugh KPIT
# FLA -> Miami KMIA
# MIN -> Minneapolis St.Paul KMSP
# CHW -> Midway KMDW
# OAK -> Oakland Airpot KOAK
# TOR -> Toronto Pearson CYYZ
# NYY -> LaGuardia KLGA
# TBR -> Tampa KTPA
# BOS -> Logan KBOS
# TEX -> Arlington Municipal KAWO
'''

'''
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

full_weather = pd.DataFrame()
airports = list(set(team_to_airport.values()))
for i in airports:
	weather = pd.read_csv('WeatherData/' + i + '_weather_data.csv')
	small_weather = pd.DataFrame()
	small_weather["Date"] = weather.Date
	small_weather["MaxTemp"] = weather.Max_TemperatureF
	small_weather["MinTemp"] = weather.Min_TemperatureF
	small_weather["MeanTemp"] = weather.Mean_TemperatureF
	small_weather["Prec"] = weather.PrecipitationIn
	small_weather["PrecEvent"] = weather.Events
	small_weather["AirportCode"] = i
	print small_weather
	full_weather = full_weather.append(small_weather)
full_weather.to_csv('full_weather.csv')
'''


'''

airport_code_list = ['KSFO','KBUR','KOAK','KCLE','KSAN','KSEA','KBOS','KSNA',
					 'KPHX','KBWI','KMDW','KSTL','KATL','KIAD','KIAH','KCVG',
					 'KMCI','KDTW','KPHL','KMKE','KMIA','KLGA','KDEN','KPIT',
					 'KMIA','KMSP','KMDW','CYYZ','KLGA','KTPA','KAWO']


# iterate results
for station in stations['list']:
    if station['name'] in airport_code_list:
    	print station['name']
    	print station['id']
    	print '\n'
'''

'''
batting = pd.read_csv('combined_batting_player_test.csv')

print batting.Home * batting.Team + (~batting.Home + 2) * batting.Opp

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
							   batting.loc[:,"Against" + i] * ~batting.Home
'''



