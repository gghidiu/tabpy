import pandas as pd
import requests
import json

#FlightAware API access data
#Currently using Raphael's private credit card. Will have to switch to a company account when in production
username = "raphaelt25"
apiKey = "3cd7c82f1548d8545a1dd795c7e850a0f05cd4b9"
fxmlUrl = "https://flightxml.flightaware.com/json/FlightXML2/"


#Fuel consumption rate for each aircraft type and each flight distance range have to be retrieved from the 
# CSV file that was prepared beforehand
fuel_rate_filepath = r"C:\Users\gghidiu\Box\Gheorghes Box Notes\Emissions Calculator\Fuel consumption per Km by aircraft type.csv"
fuel_rate_filepath_docker = 'fuel_consumption_per_km_by_aircraft_type.csv'
fuel_rate_DF = pd.read_csv(fuel_rate_filepath_docker)


def get_scheduled_fligts(origin, destination, startunixdate, endunixdate):
    #Flightaware API
    payload = {'origin':origin, 'destination':destination, 'howMany':'SetMaximumResultSize',\
               'startDate':startunixdate, 'endDate':endunixdate, 'offset':'0'}
    r = requests.get(fxmlUrl + "AirlineFlightSchedules",
        params=payload, auth=(username, apiKey))
    response = json.loads(r.text) 
    if r.status_code == 200:
        #get the nested dictioanry into dataframe
        fligts_df = pd.DataFrame(response['AirlineFlightSchedulesResult']['data'])
        return(fligts_df)
    else:
        print("Error executing request")
        


def get_total_fuel_and_seats(origin, destination, distance, start_date, end_date):
   
    #get the scheduled flights on route for the time interval
    scheduled_flights = get_scheduled_fligts(origin, destination, start_date, end_date)
    #check if the API has returned any flights
    if scheduled_flights.empty: 
        total_fuel = 0
        economy_seats = 0
    else:
        #get total number of economy seats per aircraft type
        calculation_df = scheduled_flights[['aircrafttype','seats_cabin_coach']].groupby(['aircrafttype']).sum()
        #get number of flights per aircraft type
        calculation_df['flights_per_type']= scheduled_flights['aircrafttype'].value_counts()
        #API output not needed anymore
        scheduled_flights = None  

        #get only relevant fuel counsumtion rates for this route
        larger_thatn_from_distance = distance > fuel_rate_DF['Range From (consumption rate)']
        not_larger_than_to_distance = distance <= fuel_rate_DF['Range To (consumption rate)']
        to_distance_is_null = fuel_rate_DF['Range To (consumption rate)'].isnull()
        aircraft_type = fuel_rate_DF['ICAO Code'].isin(calculation_df.index.tolist())
        relevant_rates = fuel_rate_DF[larger_thatn_from_distance & aircraft_type &\
                                          (not_larger_than_to_distance | to_distance_is_null)]
        relevant_rates = relevant_rates[['ICAO Code','Fuel consumption Kg/Km']]

        #add the rates to the calculation DF, default join is left, which leaves aircraft types on that day for that we do not have consumption data
        calculation_df = calculation_df.join(relevant_rates.set_index('ICAO Code'))
        #total fuel per aircraft column
        calculation_df['consumed_fuel'] = calculation_df['flights_per_type'] *calculation_df['Fuel consumption Kg/Km']*distance
        #filter fligts for which consumption rate is unknown
        rate_available = ~ calculation_df['Fuel consumption Kg/Km'].isnull()
        calculation_df = calculation_df[rate_available]
        #get total fuel consumed
        total_fuel = calculation_df['consumed_fuel'].sum()
        #get number of economy seats 
        economy_seats = calculation_df['seats_cabin_coach'].sum()
        calculation_df = None
    
    return total_fuel, economy_seats        
        
def return_df(input_df):
    
    '''
    the function get_total_fuel_and_seats returns a pandas series of tuples. This is done to obtain the 
    total fuel and the nuber of economy seats both in one API request, as these requests are very slow.
    This series is then split into two dataframe columns in the folowing step so that each value can be assigned 
    to a single column in tableau prep
    '''

    #creaty empty dataframe
    totalfuel_seats_df = pd.DataFrame()
    #get the series of tuples from API
    series = input_df.apply(lambda x: get_total_fuel_and_seats(x['ICAO1'],x['ICAO2'],x['Trip Distance Adj']\
                ,x['StartUnixDate'],x['EndUnixDate'],), axis=1 ).values.tolist()
                    # values.tolist() part transforms the panda series into a list
    #populate dataframe
    totalfuel_seats_df[['total_fuel','economy_seats']] = pd.DataFrame(series)
        
    #populate the dataframe from prep
    input_df.loc[:,'Number of Y-seats'] = totalfuel_seats_df['economy_seats']
    input_df.loc[:,'Total fuel'] = totalfuel_seats_df['total_fuel']
    
    
    return input_df     
