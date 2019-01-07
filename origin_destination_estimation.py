import math
import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup

def get_zip_coords():
    '''
    Scrapes data from zip-codes.com to get latitude, longitude coordinates for all zip codes within Suffolk County, Boston.
    Returns:
        zip_pop: a dictionary with zip code keys and population values
        zip_lat: a dictionary with zip code keys and latitude coordinate values
        zip_lon: a dictionary with zip code keys and longitude coordinate values
    '''
    # Initialize dictionaries that hold informative values by zip code
    zip_pop = {}
    zip_lat = {}
    zip_lon = {}
    
    # Initialize the web page containing the desired data
    page = requests.get('https://www.zip-codes.com/city/ma-boston.asp#zipcodes')
    
    # Confirm web page is successfully obtained
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser') # Instantiate BeautifulSoup object
        rows = soup.find('table', {'id' : 'tblZIP'}).find_all('tr') # Find all rows in the desired table
        
        for i in range(1, len(rows)): # For every row except the header row
            zipcode = str(rows[i].find('td').get_text('title').split(' ')[2]) # Get zip code from row
            pop = int(rows[i].find_all('td')[3].get_text('td').replace(',', '')) # Get population corresponding to zip code
            
            # Define zip code specific web page that contains the desired coordinate data
            zip_url = 'https://www.zip-codes.com/zip-code/' + zipcode + 'zip-code-' + zipcode + '.asp'
            # Initialize the zip code specific web page based on zip_url string
            zip_page = requests.get(zip_url)
            # Confirm web page is successfully obtained
            if page.status_code == 200:
                zip_soup = BeautifulSoup(zip_page.content, 'html.parser') # Instantiate BeautifulSoup object
                anomaly = 0 # Most rows in table meet the standard criteria except for a few "anomalies", which require only slightly different logic.
                try:
                    # Get latitude (this is where the latitude data is for most zip codes)
                    latitude = float(zip_soup.find_all('tr')[12].find_all('td')[1].get_text())
                except:
                    # Flag as anomaly and search in the next block down
                    latitude = float(zip_soup.find_all('tr')[13].find_all('td')[1].get_text())
                    anomaly = 1
                if anomaly == 0:
                    # Get longitude data for "normal" rows
                    longitude = float(zip_soup.find_all('tr')[13].find_all('td')[1].get_text())
                else:
                    # Get longitude data in slightly different location if zip code is flagged as an anomaly
                    longitude = float(zip_soup.find_all('tr')[14].find_all('td')[1].get_text())
                
                # Add population, latitude, and longitude of each zip code to respective dictionaries
                zip_pop[zipcode] = pop
                zip_lat[zipcode] = latitude
                zip_lon[zipcode] = longitude
            
            # If web page not successfully obtained, print error and exit
            else:
                sys.exit('Error: page not found for zip code ' + zipcode + '. Page status code is not 200.')
            
            anomaly = 0 # Reset anomaly indicator to zero for next iteration
    
    # If web page not successfully obtained, print error and exit
    else:
        sys.exit('Error: Zip Code page status code is not 200.')
    
    return zip_pop, zip_lat, zip_lon

def get_station_coords():
    '''
    Gets latitude, longitude coordinates for all MBTA stations that are included in turnstile_data.csv
    Returns:
        lat: a dictionary with MBTA station keys and latitude coordinate values
        lon: a dictionary with MBTA station keys and longitude coordinate values
    '''
    
    # Create dictionary consisting of latitude and longitude coordinates
    # Coordinates manually obtained from https://www.zip-codes.com
    coords = {'Andrew Square' : '42.33195 -71.05721',
              'JFK/U Mass' : '42.32060 -71.05237',
              'North Quincy' : '42.27581 -71.03017',
              'Wollaston' : '42.26677 -71.02051',
              'Quincy Center' : '42.25199 -71.00550',
              'South Station' : '42.35192 -71.05507',
              'Maverick' : '42.36913 -71.03954',
              'Airport' : '42.36589 -71.01755',
              'Aquarium' : '42.35922 -71.04915',
              'Wood Island' : '42.37972 -71.02294',
              'Orient Heights' : '42.38925 -71.00000',
              'Suffolk Downs' : '42.39050 -70.99712',
              'Beachmont' : '42.39720 -70.99252',
              'Revere Beach' : '42.40787 -70.99253',
              'Wonderland' : '42.41364 -70.99160',
              'Bowdoin' : '42.36137 -71.06204',
              'Braintree' : '42.20753 -71.00136',
              'Alewife' : '42.39563 -71.14190',
              'Davis Square' : '42.39672 -71.12232',
              'Porter Square' : '42.38886 -71.11940',
              'Harvard' : '42.37354 -71.11896',
              'Central Square' : '42.36533 -71.10444',
              'Kendall Square' : '42.36287 -71.09010',
              'Downtown Crossing' : '42.35550 -71.05943',
              'Savin Hill' : '42.30986 -71.04996',
              'Fields Corner' : '42.30010 -71.05783',
              'Shawmut' : '42.34327 -71.07132',
              'Ashmont' : '42.28452 -71.06379',
              'Government Center' : '42.36048 -71.05906',
              'Park Street' : '42.35706 -71.06258',
              'Boylston' : '42.34865 -71.08270',
              'Arlington' : '42.35190 -71.07071',
              'Copley Square' : '42.34832 -71.07597', 
              'Symphony' : '42.34268 -71.08505',
              'Hynes' : '42.34797 -71.08793',
              'Prudential' : '42.34568 -71.08116',
              'Kenmore Square' : '42.34889 -71.09567',
              'Science Park' : '42.36682 -71.06778',
              'Lechmere' : '42.37093 -71.07750',
              'Oak Grove' : '42.43667 -71.07110',
              'Malden Center ' : '42.42678 -71.07431',
              'Wellington ' : '42.41121 -71.08283',
              'Sullivan Square' : '42.38403 -71.07655',
              'Community College' : '42.37368 -71.06968',
              'North Station' : '42.36565 -71.06388',
              'Haymarket' : '42.36285 -71.05827',
              'State Street' : '42.35749 -71.05744',
              'Chinatown' : '42.35239 -71.06257',
              'Tufts Medical Center' : '42.34966 -71.06392',
              'Back Bay' : '42.34735 -71.07570',
              'Mass Ave' : '42.34168 -71.08329',
              'Ruggles' : '42.33665 -71.08941',
              'Roxbury Crossing' : '42.33134 -71.09550',
              'Jackson Square' : '42.32320 -71.09978',
              'Stony Brook' : '42.31727 -71.10416',
              'Green Street' : '42.31041 -71.10757',
              'Forest Hills' : '42.30069 -71.11397',
              'Riverside' : '42.33737 -71.25260',
              'Quincy Adams' : '42.23309 -71.00723',
              'Broadway' : '42.34257 -71.05694',
              'Courthouse' : '42.35226 -71.04690',
              'World Trade Center' : '42.34873 -71.04227',
              'Charles MGH' : '42.36122 -71.07054'}
    
    # Initialize dictionaries for latitude and longitude coordinates of MBTA stations
    lat = {}
    lon = {}
    
    # Splice coords into latitude and longitude
    for key in coords:
        lat[key] = float(coords[key].split(" ")[0])
        lon[key] = float(coords[key].split(" ")[1])
    
    return lat, lon

def station_dist_matrix(stations, station_lat, station_lon):
    '''
    Computes the Euclidean distances between MBTA stations
    Args:
        stations: an array of strings indicating the MBTA stations
        lat: a dictionary with MBTA station keys and latitude coordinate values
        lon: a dictionary with MBTA station keys and longitude coordinates values
    Returns:
        distance: a dataframe/matrix whose entry (i,j) represents the distance from station i to station j
    '''
    # Instantiate distance matrix as a dataframe
    distance = pd.DataFrame(columns=list(stations), index=list(stations))
    
    # Fill in distance matrix with Euclidean distances between stations
    # Note: entry (i,j) is equivalent to entry (j,i)
    for i in range(len(stations)):
        for j in range(i+1, len(stations)):
            lat_dist = station_lat[stations[i]] - station_lat[stations[j]]
            lon_dist = station_lon[stations[i]] - station_lon[stations[j]]
            # Compute distance
            dist = math.sqrt((lat_dist ** 2) + (lon_dist ** 2))
            distance.loc[stations[i]][stations[j]] = dist
            distance.loc[stations[j]][stations[i]] = dist
    
    # Add zeros along horizontal of matrix
    for i in range(len(distance)):
        distance.iloc[i][i] = 0.0
    
    return distance

def zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon):
    '''
    Computes the Euclidean distances between zip code locations to MBTA stations
    Args:
        zip_lat: a dictionary with zip code keys and latitude coordinate values
        zip_lon: a dictionary with zip code keys and longitude coordinate values
        station_lat: a dictionary with MBTA station keys and latitude coordinate values
        station_lon: a dictionary with MBTA station keys and longitude coordinate values
    Returns:
        distance: a dataframe/matrix whose entry (i,j) represents the distance from zip code i to station j
    '''
    # Get list of all unique zip codes
    zips = [key for key in zip_lat]
    # Get list of all unique MBTA stations
    stations = [key for key in station_lat]
    
    # Instantiate distance matrix as a dataframe: rows = stations, columns = zip codes
    distance = pd.DataFrame(columns=list(zips), index=list(stations))
    
    # Fill in distance matrix with Euclidean distances between zip codes and stations
    for i in range(len(zips)):
        for j in range(len(stations)):
            lat_dist = station_lat[stations[j]] - zip_lat[zips[i]]
            lon_dist = station_lon[stations[j]] - zip_lon[zips[i]]
            # Compute distance
            dist = math.sqrt((lat_dist ** 2) + (lon_dist ** 2))
            distance.loc[stations[j]][zips[i]] = dist

    return distance
    

if __name__ == '__main__':
    # Read in turnstile data
    turnstile_df = pd.read_csv('./data/turnstile_data.csv')
    # Get all unique MBTA station names for which we have turnstile data
    stations = turnstile_df.station.unique()
    
    zip_pop, zip_lat, zip_lon = get_zip_coords()
    station_lat, station_lon = get_station_coords()
    station_distances = station_dist_matrix(stations, station_lat, station_lon)
    station_zip_dist = zip_station_matrix(zip_lat, zip_lon, station_lat, station_lon)