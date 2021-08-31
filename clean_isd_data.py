import os
import pathlib
from business_logic.utils_IO_bound import rm_0_byte_files_from, retreive_file_content_from
from business_logic.utils_data_manipulation import isd_data_parser


this_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw' 

''' -------------------------------------------[ method impl ]------------------------------------------- '''
import pydantic 
from typing import Any, Dict, List, Tuple, TypeVar
from business_logic.schemas import AvgSingleDayRecords, AvgMonthlyRecords
PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)


def monthly_data_aggregation_for(weather_station_matrix_data:List[List[PydanticModel]]) -> List[List[PydanticModel]]:
    ''' takes in a matrix_data, [[dataset],...,[dataset]], and for each dataset entry aggregates into monthly avg for a year's worth of data, for each dataset in the matrix 
        Args:
            weather_station_matrix_data: list containing a year's worth of data as pydantic models 
        Returns:
            A matrix data with each dataset entry containing avgerage values for each month per weather station 
    '''
    daily_avg_matrix_data = [_aggregation_of_data_for(entry_year_worth_of_data, 'day', AvgSingleDayRecords,'air_temp', 'sea_lvl_P', 'dew_point_temp') for entry_year_worth_of_data in weather_station_matrix_data]

    return [_aggregation_of_data_for(entry_year_worth_of_data, 'month', AvgMonthlyRecords, 'avg_air_temp', 'avg_sea_lvl_P', 'avg_dew_point_temp') for entry_year_worth_of_data in daily_avg_matrix_data]


def _aggregation_of_data_for(list_of_inst_models:List[PydanticModel], time:str, schema:PydanticModel, *params:str) -> List[List[PydanticModel]]:
    ''' Aggregation of data according to datetime-time specification. Example: aggregation of data according to day or according to month 
        Args:
            list_of_inst_models: list of pydantic models 
            time: specifies how the aggregation of data will be identified by. Days, months, etc... 
            schema: pydantic schema 
            params: additional params that is used to create aggregation variables 
        Returns:
            aggregated_dataset
    '''
    aggregated_dataset = []
    tmp_dataset_container = []
    for i in range(1, len(list_of_inst_models)):
        prev_data_point_entry = list_of_inst_models[i - 1]
        curr_data_point_entry = list_of_inst_models[i]
        if len(tmp_dataset_container) == 0:
            tmp_dataset_container.append(prev_data_point_entry)
        if getattr(prev_data_point_entry.date, time) == getattr(curr_data_point_entry.date, time):
            tmp_dataset_container.append(curr_data_point_entry)
        else: 
            avg_for_single_day_inst_model = _data_point_avg_for(tmp_dataset_container,schema,*params)
            aggregated_dataset.append(avg_for_single_day_inst_model)
            tmp_dataset_container = []
    return aggregated_dataset


def _data_point_avg_for(list_of_inst_models:List[PydanticModel], schema:PydanticModel, *params:str) -> PydanticModel:
    '''performs the creation of key-value pair and averaging of params of interest 
        Args:
            list_of_inst_models: list of pydantic models 
            schema: pydantic schema 
            params: additional params that is used to create aggregation variables 
        Returns:
            avg_inst_model
    '''
    tmp_record = {
        'usaf': list_of_inst_models[0].usaf,
        'wban': list_of_inst_models[0].wban,
        'date': list_of_inst_models[0].date,
        'lat': list_of_inst_models[0].lat,
        'lon': list_of_inst_models[0].lon,
    }
    for data_point_entry in list_of_inst_models:
        for param in params:
            if param not in tmp_record.keys():
                tmp_record[param] = int(getattr(data_point_entry, param))
            else: 
                tmp_record[param] += int(getattr(data_point_entry, param)) 
    for param in params:
        tmp_record[param] = tmp_record[param] / len(list_of_inst_models)
    avg_inst_model = schema(**tmp_record)
    return avg_inst_model

''' -------------------------------------------[ method impl ]------------------------------------------- '''

''' this script only contains application logic '''
def main():
    rm_0_byte_files_from(raw_dir) 
    num_of_files, dir_content_dict = retreive_file_content_from(raw_dir)
    weather_station_matrix_data = isd_data_parser(num_of_files, dir_content_dict) 
    aggregated_weather_station_data = monthly_data_aggregation_for(weather_station_matrix_data)
    ''' NOTE it seems like i am getting the right data but before concluding clean up the code and run test to ensure that you are getting the correct data '''
    print('\n----------[ START ]----------\n')
    print(aggregated_weather_station_data[0][0] )
    print(aggregated_weather_station_data[0][1] )
    print(aggregated_weather_station_data[0][2] )
    print('\n----------[ END ]----------\n')


if __name__ == '__main__': 
    main() 
''' NOTE NOTE IMPORTANT TO DOCUMENT THERE CAN ONLY BE ONE LOGGER.INFO, LOGGER.ERROR, LOGGER.WARNING PER SCRIPT BUT YOU CAN HAVE AS MANY PRINT AS YOU WANT  NOTE NOTE '''

'''  
    NOTE FRI-12:15PM 8/27 - steps to cleaning ISD data 

        >>> NOTE BUG "Each station's monthly aggregated data should be written to its own seperate json file in a subfolder of project_data called monthly-weather-data with the naming scheme {usaf}-{wban}.json"
'''