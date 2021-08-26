import pydantic 
from typing import Dict, List, Tuple, TypeVar
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

def weather_station_yealy_data(num_of_files: int, file_content_dict:Dict[str,List[bytes]]) -> List[List[PydanticModel]]: #NOTE UPDATE DOCS
    ''' 
        Args:
            
        Returns:
            
    '''
    return [_isd_parser_for(file_name, file_content_obj, num_of_files) for file_name, file_content_obj in file_content_dict.items()]


def _isd_parser_for(file_name:str, file_content_obj:Dict[str,Tuple[str,List[bytes]]], num_of_files:int) -> List[PydanticModel]: #NOTE UPDATE DOCS
    ''' takes a list of line data from a gz file and converts into list of pydantic model 
        Args:
            file_content: list of bytes data in a given gz file 
        Returns:
            list of pydantic models 
            {file_num: file_content}
    '''
    list_of_dict_objs = []
    file_num = file_content_obj['file_content'][0]
    file_content = file_content_obj['file_content'][1]
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
        list_of_dict_objs.append(WeatherStationRecord(**dict_obj))
    return list_of_dict_objs
