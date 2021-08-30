import os
import pathlib
from business_logic.utils_IO_bound import rm_0_byte_files_from, retreive_file_content_from
from business_logic.utils_data_manipulation import isd_data_parser


this_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw' 

''' -------------------------------------------[ method impl ]------------------------------------------- '''
import pydantic 
from typing import Any, Dict, List, Tuple, TypeVar
from business_logic.schemas import AvgSingleDayRecords
PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)
def monthly_data_aggregation_for(weather_station_matrix_data:List[List[PydanticModel]]) -> List[List[PydanticModel]]:
    ''' takes in a matrix_data, [[dataset],...,[dataset]], and for each dataset entry aggregates into monthly avg for a year's worth of data, for each dataset in the matrix 
        Args:
            weather_station_matrix_data: list containing a year's worth of data as pydantic models 
        Returns:
            NOTE NOTE TO BE DETERMINED NOTE NOTE
    '''
    daily_avg_matrix_data = [_aggregation_of_data_to_day_avg_for(entry_year_worth_of_data) for entry_year_worth_of_data in weather_station_matrix_data]
    return [_aggregation_of_data_to_monthly_avg_for(entry_year_worth_of_data) for entry_year_worth_of_data in daily_avg_matrix_data]


def _aggregation_of_data_to_day_avg_for(entry_year_worth_of_data:List[PydanticModel]) -> List[PydanticModel]:
    ''' takes a year's worth of data for a given weather station and aggregates it by monthly avg 
        Args:
            entry_year_worth_of_data: list of pydantic inst models 
        Returns:
            day_avg: a years worth of data with each entry being the avgerage for a given day 
    '''
    single_day_worth_of_data = []
    day_avg = []
    for i in range(1,len(entry_year_worth_of_data)):
        prev_data_point_entry = entry_year_worth_of_data[i - 1] #data_point_entry are inst_model 
        curr_data_point_entry = entry_year_worth_of_data[i]
        if len(single_day_worth_of_data) == 0:
            single_day_worth_of_data.append(prev_data_point_entry)
        if prev_data_point_entry.date.day == curr_data_point_entry.date.day:
            single_day_worth_of_data.append(curr_data_point_entry)
        else: 
            avg_for_single_day_inst_model = _data_point_avg_for(single_day_worth_of_data)
            day_avg.append(avg_for_single_day_inst_model)
            single_day_worth_of_data = []
    return day_avg


def _aggregation_of_data_to_monthly_avg_for(entry_year_worth_of_data:List[PydanticModel]) -> List[List[PydanticModel]]:
    ''' iterates through a years worth of records for a single weather station. Aggregate daily avgerage records into monthly average records. 
        Args:
            entry_year_worth_of_data
        Returns:
            
    '''
    monthly_avg_records = []
    single_month_worth_of_data = []
    for i in range(1, len(entry_year_worth_of_data)):
        prev_data_point_entry = entry_year_worth_of_data[i - 1]
        curr_data_point_entry = entry_year_worth_of_data[i]
        ''' 1 1 1 2 2 3 4 '''
        if len(single_month_worth_of_data) == 0:
            single_month_worth_of_data.append(prev_data_point_entry)
        if prev_data_point_entry.date.month == curr_data_point_entry.date.month:
            single_month_worth_of_data.append(curr_data_point_entry)
        else: 
            avg_for_single_day_inst_model = _data_point_avg_for(single_month_worth_of_data)
            monthly_avg_records.append(avg_for_single_day_inst_model)
            single_month_worth_of_data = []
    return monthly_avg_records


def _data_point_avg_for(single_day_worth_of_data:List[PydanticModel]) -> PydanticModel:
    '''this piece of business logic will itr thr a single_day_worth_of_data, sum the air_temp, sea_lvl_P, and dew_point_temp, and divide by the total_num_of_records recorded on a single day -> you will have a py_dict_obj that holds the summarized data for which you need to convert into a pydantic inst model <=> you will need to create another schema, build a convertor method pydantic_converter_of(data:Dict,schema:Type[TPydanticModel]) -> PydanticModel
    NOTE NOTE update the doc str NOTE NOTE
        Args:
            
        Returns:
            returns a single PydanticModel inst model 
    '''
    avg_for_single_day = {
        'usaf': single_day_worth_of_data[0].usaf,
        'wban': single_day_worth_of_data[0].wban,
        'date': single_day_worth_of_data[0].date,
        'lat': single_day_worth_of_data[0].lat,
        'lon': single_day_worth_of_data[0].lon,
        'avg_air_temp': 0,
        'avg_sea_lvl_P': 0,
        'avg_dew_point_temp': 0,
    }
    print('\n----------[ START ]----------\n')
    print(type(avg_for_single_day['date']))
    print('\n----------[ END ]----------\n') 
    for data_point_entry in single_day_worth_of_data:
        avg_for_single_day['avg_air_temp'] += int(data_point_entry.air_temp)
        avg_for_single_day['avg_sea_lvl_P'] += int(data_point_entry.sea_lvl_P)
        avg_for_single_day['avg_dew_point_temp'] += int(data_point_entry.dew_point_temp)
    avg_for_single_day['avg_air_temp'] = avg_for_single_day['avg_air_temp']/len(single_day_worth_of_data)
    avg_for_single_day['avg_sea_lvl_P'] = avg_for_single_day['avg_sea_lvl_P']/len(single_day_worth_of_data)
    avg_for_single_day['avg_dew_point_temp'] = avg_for_single_day['avg_dew_point_temp']/len(single_day_worth_of_data)
    avg_for_single_day_inst_model = AvgSingleDayRecords(**avg_for_single_day)
    return avg_for_single_day_inst_model


''' -------------------------------------------[ method impl ]------------------------------------------- '''

''' this script only contains application logic '''
def main():
    rm_0_byte_files_from(raw_dir) 
    num_of_files, dir_content_dict = retreive_file_content_from(raw_dir)
    weather_station_matrix_data = isd_data_parser(num_of_files, dir_content_dict) 
    aggregated_weather_station_data = monthly_data_aggregation_for(weather_station_matrix_data)
    print('\n----------[ START ]----------\n')
    print(aggregated_weather_station_data )
    print('\n----------[ END ]----------\n') 

if __name__ == '__main__': 
    main() 
''' NOTE NOTE IMPORTANT TO DOCUMENT THERE CAN ONLY BE ONE LOGGER.INFO, LOGGER.ERROR, LOGGER.WARNING PER SCRIPT BUT YOU CAN HAVE AS MANY PRINT AS YOU WANT  NOTE NOTE '''

'''  
    NOTE FRI-12:15PM - steps to cleaning ISD data 

        - a weather station will have multiple records recorded on a single day 
            ⮑ what needs to be done here is to sum the records that can be summed up and divide by the number of records found for a given day 
                ⮑ this requires an algo that can check to see the date 
                    ⮑ if the date given is on the same day then it continues summing values otherwise it closes the summing and performs the avg calculation and then moves to begin summing for the next day 
                
        - [3] monthly_aggregated_data will be saved to a list_of_monthly_aggregated_data 
            ⮑ [
                [
                    station_1_jan_2016, 
                    station_1_feb_2016, 
                    ...
                    station_1_dec_2016
                ],
                ...
                [
                    station_n_jan_20xx, 
                    station_n_feb_20xx, 
                    ...
                    station_n_dec_20xx
                ],
            ]
        
        >>> NOTE BUG "Each station's monthly aggregated data should be written to its own seperate json file in a subfolder of project_data called monthly-weather-data with the naming scheme {usaf}-{wban}.json"
'''