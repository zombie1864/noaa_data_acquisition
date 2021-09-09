import pydantic 
from typing import Any, Dict, List, Tuple, TypeVar
from business_logic.schemas import WeatherStationRecord, AvgSingleDayRecords, AvgMonthlyRecords


PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)

''' -----------------------------[ fetch_ftp related methods ]----------------------------- '''

def weather_stations_by(start:int, end:int, list_of_models:List[PydanticModel]) -> List[str]: 
    '''  performs a filtering of pydantic models that encapudalte the starting year, years gte start and years lte start and returns a list of str representing weather stations 
        Args:
            start: starting year to which the filtering is being performed by 
            end: ending year to which the filtering is being performed by 
        Returns:
            list of weather station 
    '''
    return [model.USAF + '-' + model.WBAN for model in list_of_models if model.BEGIN.year <= start and model.END.year == end - 1]

            
''' -----------------------------[ cleaning_isd related methods ]----------------------------- '''

def isd_data_parser(num_of_files: int, dir_content_dict:Dict[str,Tuple[Any]]) -> List[List[PydanticModel]]: 
    ''' this is an isd parser which translates noaa's isd temperature data into a pydantic model. A parser in general turns a string, binary data, etc. into a data structure. The goal is to return an n dimensional matrix containing a years worth of data as a list of pydantic inst models for a single weather station. [[weather_station_data_1], ..., [weather_station_data_n]]
        Args:
            num_of_files: the total number of files in a dir containg `.gz` files 
            dir_content_dict: py dict containing file_name as key and tuple(file_num, file_content) where file_content is a list of bytes for a given `.gz` file 
        Returns:
            weather_station_matrix_data - List[List[PydanticModel]]
    '''
    return [_isd_parser_for(file_name, file_content_tuple, num_of_files) for file_name, file_content_tuple in dir_content_dict.items()]


def _isd_parser_for(file_name:str, file_content_tuple:Tuple[str,List[bytes]], num_of_files:int) -> List[PydanticModel]: 
    ''' takes a list of line data from a gz file and converts into list of pydantic model 
        Args:
            file_name: name of the file ex: 123-456.gz 
            file_content_tuple: tuple containing the file_num and the content inside .gz file 
            num_of_files: the total number of files inside the dir housing the raw .gz file data 
        Returns:
            a single weather station's year worth of data as pydantic inst models
    '''
    year_worth_of_weather_station_data = []
    file_num, file_content = file_content_tuple
    print(f'parsing data for {file_name} file number: {file_num} out of {num_of_files}')
    for line_data in file_content[:-1]:
        str_line_data = line_data.decode('utf-8')
        dict_obj = {
            'usaf': str_line_data[4:10],
            'wban': str_line_data[10:15],
            'date': str_line_data[15:23],
            'lat': str_line_data[28:34],
            'lon': str_line_data[34:41],
            'air_temp': str_line_data[87:92],
        } 
        year_worth_of_weather_station_data.append(WeatherStationRecord(**dict_obj))
    return year_worth_of_weather_station_data


def monthly_data_aggregation_for(weather_station_matrix_data:List[List[PydanticModel]]) -> List[List[PydanticModel]]:
    ''' takes in a matrix_data, [[dataset],...,[dataset]], and for each dataset entry aggregates into monthly avg for a year's worth of data, for each dataset in the matrix 
        Args:
            weather_station_matrix_data: list containing a year's worth of data as pydantic models 
        Returns:
            A matrix data one with each dataset entry containing avgerage values for each month per weather station
            [[avg_for_jan],...,[avg_for_dec]]
    '''
    daily_avg_matrix_data = [ _aggregation_of_data_for(entry_year_worth_of_data, 'day', AvgSingleDayRecords,'air_temp') for entry_year_worth_of_data in weather_station_matrix_data]

    return [_aggregation_of_data_for(daily_avg_year_worth_of_data, 'month', AvgMonthlyRecords, 'avg_air_temp') for daily_avg_year_worth_of_data in daily_avg_matrix_data]


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
            avg_for_single_time_period_inst_model = _data_point_avg_for(tmp_dataset_container,schema,*params)
            aggregated_dataset.append(avg_for_single_time_period_inst_model)
            tmp_dataset_container = []
    return aggregated_dataset


def _data_point_avg_for(list_of_inst_models:List[PydanticModel], schema:PydanticModel, *params:str) -> PydanticModel:
    '''creates an avg pydantic inst model for a single dataset. Ex the avg for a single day - avgeraging all records for a single day 
        Args:
            list_of_inst_models: list of pydantic models 
            schema: pydantic schema 
            params: additional params that is used to create aggregation variables 
        Returns:
            avg_inst_model: a pydantic inst model 
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
        if param == 'air_temp': 
            tmp_record[param] = tmp_record[param] / 10
    avg_inst_model = schema(**tmp_record)
    return avg_inst_model

def rm_0_len_weather_station_data_for(aggregated_weather_station_data:List[List[PydanticModel]]) -> List[List[PydanticModel]]: 
    ''' returns a filtered aggregated weather station data in which elements in the matrix data of lenth zero are removed
        Args:
            aggregated_weather_station_data: A matrix data 
        Returns:
            A matrix data in which elements of length zero are removed 
    '''
    return [weather_station for weather_station in aggregated_weather_station_data if len(weather_station) != 0]