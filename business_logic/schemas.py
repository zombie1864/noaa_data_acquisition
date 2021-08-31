import pydantic
from datetime import datetime

def format_wban(str_obj:str) -> None:#NOTE this should be in data_manip 
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


class AvgSingleDayRecords(pydantic.BaseModel):
    ''' avg_for_single_day schema '''
    usaf: str
    wban: str
    date: datetime
    lat: str
    lon: str
    avg_air_temp: float = pydantic.Field(..., alias='air_temp')
    avg_sea_lvl_P: float = pydantic.Field(..., alias='sea_lvl_P')
    avg_dew_point_temp: float = pydantic.Field(..., alias='dew_point_temp')


class AvgMonthlyRecords(pydantic.BaseModel):
    ''' avg_for_single_day schema '''
    usaf: str
    wban: str
    date: datetime
    lat: str
    lon: str
    avg_air_temp: float = pydantic.Field(..., alias='air_temp')
    avg_sea_lvl_P: float = pydantic.Field(..., alias='sea_lvl_P')
    avg_dew_point_temp: float = pydantic.Field(..., alias='dew_point_temp')