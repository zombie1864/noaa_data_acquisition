import pytest 
import ftplib
import json
from unittest import mock
from ..schemas import format_wban
from ..utils_data_manipulation import weather_stations_by
from ..utils_file_IO import fetch_noaa_ftp_data, _fetch_files
from ..schemas import StationMetadataModel
from ..fileio import CsvReader, JsonWriter
from unittest import mock
  

def test_CsvReader(mock_csv_file_path, csv_schema):
    list_of_inst_models = CsvReader().read(mock_csv_file_path, csv_schema)
    assert isinstance(list_of_inst_models[0], csv_schema)


def test_JsonWriter(tmp_path, list_of_inst_models):
    tmp_dir_path = tmp_path / 'sub'
    tmp_dir_path.mkdir()
    tmp_file_path = tmp_dir_path / 'test_jsonwriter.json'
    JsonWriter().write(list_of_inst_models, tmp_file_path)
    res = [
        {   
            'USAF': '1234',
            'WBAN': '00005',
            'STATION_NAME': 'demo_station',
            'CTRY': 'USA',
            'STATE': 'NY',
            'ICAO': 'icao',
            'LAT': '1.23',
            'LON': '-4.56',
            'ELEV': '123',
            'BEGIN': '19890218',
            'END': '20210823',
        }
    ]
    assert json.load(open(tmp_file_path,'r')) == res


def test_format_wban():
    test_cases = ['','1','12','123','1234','12345','123456']
    assert format_wban(test_cases[0]) == '00000'
    assert format_wban(test_cases[1]) == '00001'
    assert format_wban(test_cases[2]) == '00012'
    assert format_wban(test_cases[3]) == '00123'
    assert format_wban(test_cases[4]) == '01234'
    assert format_wban(test_cases[5]) == '12345'
    assert format_wban(test_cases[6]) == '123456'


def test_fetch_noaa_ftp_data(tmp_path, mock_csv_file_path):
    tmp_dir_path = tmp_path / 'sub'
    tmp_dir_path.mkdir()
    assert fetch_noaa_ftp_data(1989,2021,tmp_dir_path,mock_csv_file_path) == None 


def test_weather_stations_by(list_of_weather_station_models):
    res = ['123-00001']
    assert weather_stations_by(2010, 2022, list_of_weather_station_models) == res 


def test_fetch_files(mocker, tmp_path):
    tmp_dir_path = tmp_path / 'sub'
    tmp_dir_path.mkdir()
    mocker.patch('ftplib.FTP')
    _fetch_files('ftp.server.local', 'pub/files', 'wanted_file.txt', tmp_dir_path)
    with open(tmp_dir_path / "wanted_file.txt") as original:
        with open("wanted_file.txt") as downloaded:
            assert original.read() == downloaded.read()


@mock.patch("ftplib.FTP") 
def test_fetch_files_exception(mock_ftp, tmp_path):
    mock_ftp.return_value.__enter__.return_value.retrbinary.side_effect = ftplib.error_perm
    tmp_dir_path = tmp_path / 'sub'
    tmp_dir_path.mkdir()
    with pytest.raises(Exception) as error:
        _fetch_files('ftp.server.local', 'pub/files', '123.gz', tmp_dir_path)
        assert str(error.value) == '123.gz not found'


def test_StationMetadataModel():
    csv_obj = {
        'USAF': '1234', 
        'WBAN': '5', 
        'STATION NAME': 'demo_station', 
        'CTRY': 'USA', 
        'STATE': 'NY', 
        'ICAO': 'icao', 
        'LAT': '1.23', 
        'LON': '-4.56', 
        'ELEV(M)': '123', 
        'BEGIN': '19890218', 
        'END': '20210823'
    }
    model_inst = StationMetadataModel(**csv_obj) 
    assert isinstance(model_inst, StationMetadataModel)
