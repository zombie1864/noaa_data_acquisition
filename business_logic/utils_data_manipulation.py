import pydantic 
from typing import Any, Dict, List, Tuple, TypeVar
from business_logic.schemas import WeatherStationRecord


PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)

''' fetch_ftp related methods '''

def weather_stations_by(start:int, end:int, list_of_models:List[PydanticModel]) -> List[str]: 
    '''  performs a filtering of pydantic models that encapudalte the starting year, years gte start and years lte start and returns a list of str representing weather stations 
        Args:
            start: starting year to which the filtering is being performed by 
            end: ending year to which the filtering is being performed by 
        Returns:
            list of weather station 
    '''
    return [model.USAF + '-' + model.WBAN for model in list_of_models if model.BEGIN.year <= start and model.END.year == end - 1]

            
''' cleaning_isd related methods '''

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
            'sea_lvl_P': str_line_data[99:104],
            'dew_point_temp': str_line_data[93:98],
        } 
        year_worth_of_weather_station_data.append(WeatherStationRecord(**dict_obj))
    return year_worth_of_weather_station_data
