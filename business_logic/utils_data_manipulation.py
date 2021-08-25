from typing import List, TypeVar
import pydantic 

TPydanticModel = TypeVar('TPydanticModel', bound=pydantic.BaseModel)

def weather_stations_by(start:int, end:int, list_of_models:List[TPydanticModel]) -> List[str]: 
    '''  performs a filtering of pydantic models that encapudalte the starting year, years gte start and years lte start and returns a list of str representing weather stations 
        Args:
            start: starting year to which the filtering is being performed by 
            end: ending year to which the filtering is being performed by 
        Returns:
            list of weather station 
    '''
    return [model.USAF + '-' + model.WBAN for model in list_of_models if model.BEGIN.year <= start and model.END.year == end - 1]


def format_wban(str_obj:str) -> None:
    ''' ensures the wban format is of length 5 
        Args:
            str_obj: wban to be formated, ex wban = 123, returns 00123
        Returns:
            returns the wban regardless of formating 
    '''
    if  len(str_obj) < 5: 
        while len(str_obj) != 5:
            str_obj = '0' + str_obj
    return str_obj
            
