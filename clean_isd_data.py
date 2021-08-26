import os
import pathlib
from business_logic.utils_IO_bound import rm_0_byte_files_from, retreive_file_content_from
from business_logic.utils_data_manipulation import weather_station_yealy_data


this_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir = pathlib.Path(this_dir) / 'business_logic' / 'project_data' / 'raw' 


''' this script only contains application logic '''
def main():
    rm_0_byte_files_from(raw_dir) 
    num_of_files, file_content_dict = retreive_file_content_from(raw_dir) #NOTE slower maybe list comprehension 
    list_of_weather_station_yearly_data = weather_station_yealy_data(num_of_files, file_content_dict) #NOTE very slow 

if __name__ == '__main__': 
    main() 
''' NOTE NOTE IMPORTANT TO DOCUMENT THERE CAN ONLY BE ONE LOGGER.INFO, LOGGER.ERROR, LOGGER.WARNING PER SCRIPT BUT YOU CAN HAVE AS MANY PRINT AS YOU WANT  NOTE NOTE '''


'''  
    NOTE WED-11:50AM - steps to cleaning ISD data 

        - [goal] list_of_monthly_aggregated_data = file_aggregation_for(raw:Any) -> monthly_aggregated_data
        
        
        - [2] pass list_of_inst_models to data_aggregation_for(list_of_inst_models) -> monthly_aggregated_data:List[PydanticModel]
            ⮑ data_aggregation_for(list_of_inst_models:List[PydanticModel]) -> List[PydanticModel]
                - creates a list holding a station's monthly data 
                    ⮑ [
                        station_1_jan_2016, 
                        station_1_feb_2016, 
                        ...
                        station_1_dec_2016
                    ]
                    >>> NOTE BUG what exactly is being "averaged"
        
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

    NOTE 3:55PM 
        - the following will be a guide to how to read the in-line data for each gz file 
    
    EXAMPLE: 
        0084720304647522016010100154+40138-075265FM-15+009299999V0209999C000019999999N016093199+00601+00001999999ADDMA1102001999999REMMET057METAR KLOM 010015Z AUTO 00000KT 10SM 06/00 A3012 RMK AO1=
    
    EXAMPLE [editable]: 
        [0084]-[720304]-[64752]-[20160101]-[0015]-[4]-[+40138]-[-075265]-[FM-15]-[+0092]-[99999]-[V020]-[9999C000019999999N016093199+00601+00001999999ADDMA1102001999999REMMET057METAR KLOM 010015Z AUTO 00000KT 10SM 06/00 A3012 RMK AO1=

    NOTE   
        - the way to read the line data above will be divided into position with the first being at index 1 rather than 0 since the line data is not program 

        - POS: [1-4 | 0:4] NOTE [plz disregard this section]
            from EXAMPLE: 0084
        
        - POS: 5-10 | 4:10 [USAF]
            from EXAMPLE: 720304
                rep: USAF (str)
        
        - POS: 11-15 | 10:15 [WBAN]
            from EXAMPLE: 64752
                rep: WBAN (int)
        
        - POS: 16-23 | 15:23 [DATE]
            from EXAMPLE: 20160101
                rep: DATE (iso format -> YYYY-mm-dd)
        
        - POS: 24-27 | [TIME] NOTE [plz disregard this section]
            from EXAMPLE: 0015
                rep: TIME (HHMM, based on UTC MIN: 0000 MAX: 2359)
        
        - POS: 28-28 | [DATA_SOURCE_FLAG] NOTE [plz disregard this section]
            from EXAMPLE: 4
                rep: DATA_SOURCE_FLAG (categorical*, MIN: 1  MAX: Z)
        
        - POS: 29-34 | [LAT]
            from EXAMPLE: +40138
                rep: LAT (int)
        
        - POS: 35-41 | [LON]
            from EXAMPLE: -075265
                rep: LON (int)
        
        - POS: 42-46 | [CODE] NOTE [plz disregard this section]
            from EXAMPLE: FM-15
                rep: CODE (categorical)
        
        - POS: 47-51 | [ELEV] NOTE [plz disregard this section]
            from EXAMPLE: +0092
                rep: ELEV (int)
        
        - POS: 52-56 | [CALL_LETTER] NOTE [plz disregard this section]
            from EXAMPLE: 99999
                rep: CALL_LETTER (str)
        
        - POS: 57-60 | [Q_C_PROCESS] NOTE [plz disregard this section]
            from EXAMPLE: V020
                rep: Q_C_PROCESS (categorical)
        
        - POS: 61-63 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 64-64 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 65-65 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 66-69 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 70-70 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 71-75 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 76-76 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 77-77 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 78-78 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 79-84 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 85-85 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 86-86 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 87-87 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 88-92 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 93-93 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 94-98 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 99-99 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 100-104 []
            from EXAMPLE: 
                rep:  ()
        
        - POS: 105-105 []
            from EXAMPLE: 
                rep:  ()

'''