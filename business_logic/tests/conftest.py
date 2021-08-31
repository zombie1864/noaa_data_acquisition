import pytest 
import pydantic 
from business_logic.schemas import format_str_to_datetime, format_wban

@pytest.fixture
def mock_csv_data():
    return [
        'USAF,WBAN,STATION NAME,CTRY,STATE,ICAO,LAT,LON,ELEV(M),BEGIN,END', 
        '1234,5,demo_station,USA,NY,icao,1.23,-4.56,123,19890218,20210823'
    ]

@pytest.fixture
def mock_csv_file(tmp_path, mock_csv_data):
    file_path = tmp_path / "file.csv"
    file_path.write_text("\n".join(mock_csv_data))
    return file_path

@pytest.fixture 
def list_of_weather_station_models():
    class FakeWeatherStationModel(pydantic.BaseModel):
        USAF:str 
        WBAN:str
        BEGIN:str 
        END:str
        wban_validation = pydantic.validator('WBAN', allow_reuse=True)(format_wban)
        begin_validation = pydantic.validator('BEGIN', allow_reuse=True)(format_str_to_datetime)
        end_validation = pydantic.validator('END', allow_reuse=True)(format_str_to_datetime)
    return [
        FakeWeatherStationModel(USAF='123', WBAN='1', BEGIN='19890218', END='20210815'), 
        FakeWeatherStationModel(USAF='456', WBAN='2', BEGIN='20120727', END='20210815')
    ]