import os
import pathlib
from business_logic.utils_file_IO import rm_0_byte_files_from, retreive_file_content_from
from business_logic.utils_data_manipulation import isd_data_parser, monthly_data_aggregation_for


this_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw' 

''' this script only contains application logic '''
def main():
    rm_0_byte_files_from(raw_dir) 
    num_of_files, dir_content_dict = retreive_file_content_from(raw_dir)
    weather_station_matrix_data = isd_data_parser(num_of_files, dir_content_dict) 
    aggregated_weather_station_data = monthly_data_aggregation_for(weather_station_matrix_data)
    save_to_json_files_for(aggregated_weather_station_data)


if __name__ == '__main__': 
    main() 
''' NOTE NOTE IMPORTANT TO DOCUMENT THERE CAN ONLY BE ONE LOGGER.INFO, LOGGER.ERROR, LOGGER.WARNING PER SCRIPT BUT YOU CAN HAVE AS MANY PRINT AS YOU WANT  NOTE NOTE '''

'''  
    NOTE FRI-12:15PM 8/27 - steps to cleaning ISD data 
    NOTE TUE-9:00AM 9/7 - steps to creating json files for each weather station 

        >>> NOTE BUG "Each station's monthly aggregated data should be written to its own seperate json file in a subfolder of project_data called monthly-weather-data with the naming scheme {usaf}-{wban}.json the final schema should look like the following"
[
    {
        "usaf" : str   // part1 of station identifier
        "wban" : str  // part2 of station identifier
        "month" : int  
        "year" : int 
        "lat": float  // the latitude
        "lon": float  // the longitude
        "measures": [
            {
                "name": str   // ex. avg-air-temperature, avg-dewpoint-temperature ...  
                "unit": str   // temperature should be in degrees F, sea-level pressure should be in hPa
                "value": float, 
            }, 
            ...
        ] 
    }, 
    ...

]
            - create dir named "monthly-weather-data"
            - itr thr aggregated_weather_station_data 
                ⮑ single entry looks like this :
                    usaf='720324' wban='64753' date=datetime.datetime(2021, 1, 1, 0, 0) lat='+40435' lon='-075382' avg_air_temp=50.54838709677419 avg_sea_lvl_P=99999.0 avg_dew_point_temp=60.645161290322584
                        ⮑ using an algo to seperate avg_air_temp, avg_sea_lvl_P, and avg_dew_point_temp into there own category 

'''