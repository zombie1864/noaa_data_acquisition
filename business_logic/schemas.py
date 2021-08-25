import pydantic
from datetime import datetime
from business_logic.utils_data_manipulation import format_wban

def format_str_to_datetime(str_obj:str) -> datetime:
    ''' converts str text containing "yearmonthday" into datetime object 
        Args:
            str_obj: text to be converted to datetime object 
        Returns:
            datetime object 
    '''
    return datetime.strptime(str_obj, '%Y%m%d')


class StationMetadataModel(pydantic.BaseModel):
    ''' station metadata schema '''
    USAF : str 
    WBAN : str
    STATION_NAME : str = pydantic.Field(..., alias='STATION NAME')
    CTRY : str
    STATE : str
    ICAO : str
    LAT : float
    LON : float
    ELEV : str = pydantic.Field(..., alias='ELEV(M)')
    BEGIN : str
    END: str
    wban_validation = pydantic.validator('WBAN', allow_reuse=True)(format_wban)
    begin_validation = pydantic.validator('BEGIN', allow_reuse=True)(format_str_to_datetime)
    end_validation = pydantic.validator('END', allow_reuse=True)(format_str_to_datetime)


class WeatherStationRecord(pydantic.BaseModel):
    ''' schema for intermediate record building '''
    usaf: str
    wban: str
    date: str
    lat: str
    lon: str
    air_temp: str
    sea_lvl_P: str
    dew_point_temp: str
    date_validation = pydantic.validator('date', allow_reuse=True)(format_str_to_datetime)