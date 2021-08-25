""" 
One of the nice things about python is that a class is in and of itself an object. We can leverage 
this to create modularity in our library code. 
This module should implement Reader and Writer interfaces for both json and csv files that 
should be designed to work specifically with pydantic model classes. 
By using pydantic here we can lean on the some of that libraries features such as built in validation and (de)serialization.
You should end up with 4 concrete subclasses: 
    - JsonReader 
    - JsonWriter 
    - CsvReader 
    - CsvWriter 
OR as an alternative you can use multiple inheritance in order to end up with 2 concrete subclasses: 
    - JsonReaderWriter 
    - CsvReaderWriter 
    
These classes should be used in the exercises and applications in this module and be able to work with 
any type of valid data. All exercises and applications will be concerned with writing in lists or groups of 
data so these two read and write ops will suffice.
This method of API building is an example of what's called the Interface Segregation Principle. Basically 
this states that you should strive to create small abstract interfaces with very narrow functionality to increase 
flexibility. 
You should almost universally use `with` statements to handle your file I/O! This assures that if an exception happens 
during read/write that the file handle gets closed.
"""

'''  
fileio

both writer interfaces are not actual using the specified pydantic model types nor are types being checked.
'''

import pydantic
import abc 
import pathlib
import json 
import csv 
from typing import List, Type, TypeVar


# This funny business declares a custom type to use with our interface. It basically 
# says the parameter takes a *class* that is a subclass of pydantic.BaseModel not an instance of a 
# subclass of pydantic.BaseModel
TPydanticModel = TypeVar('TPydanticModel', bound=pydantic.BaseModel)


class PydanticReader(abc.ABC): 

    @abc.abstractmethod
    def read(self, filepath: pathlib.Path, model_class: Type[TPydanticModel]) -> List[TPydanticModel]: 
        """Given a valid pathlib.Path and a pydantic model class, read in a file and return a list of pydantic model instances 
        of the given type.

        Args:
            filepath (pathlib.Path): path to some file 
            model_class (TPydanticModel): A subclass of pydantic.BaseModel

        Returns:
            List[TPydanticModel]: Returns instances of the given subclass
        """
        pass 



class PydanticWriter(abc.ABC): 

    @abc.abstractmethod
    def write(self, data: List[TPydanticModel], filepath: pathlib.Path) -> None:
        """Given some data as a list of PydanticModels, writes to a file. 

        Args:
            data (List[TPydanticModel]): A list of pydantic models to write 
            filepath (pathlib.Path): The filepath to write to.
        """
        pass



class JsonReader(PydanticReader):
    ''' 
    class with read from memory interface. Supplied with valid filepath and model class returns a list of class object of desired model class 
    ex List[<class 'FakeEnergyFacilityModel'>]
    '''
    def read(self, filepath: pathlib.Path, model_class: Type[TPydanticModel]) -> List[TPydanticModel]:
        """Given a valid pathlib.Path and a pydantic model class, read in a file and return a list of pydantic model instances 
        of the given type.

        Args:
            filepath (pathlib.Path): path to some file 
            model_class (TPydanticModel): A subclass of pydantic.BaseModel

        Returns:
            List[TPydanticModel]: Returns instances of the given subclass
        """
        with open(filepath) as json_file: 
            list_of_dict_data = json.load(json_file) # convert to dict
            list_of_inst_models = [model_class(**{key: value for key, value in dict_obj.items()}) for dict_obj in list_of_dict_data]
        return list_of_inst_models 


class JsonWriter(PydanticWriter):
    def write(self, data: List[TPydanticModel], filepath: pathlib.Path) -> None:
        """Given some data as a list of PydanticModels, writes to a file. 

        Args:
            data (List[TPydanticModel]): A list of pydantic models to write 
            filepath (pathlib.Path): The filepath to write to.
        """
        list_of_json = [model_obj.json() for model_obj in data]#converts pydantic models
        with open(filepath, 'w') as f:  
            joined_str = ','.join(list_of_json)
            f.write(f'[{joined_str}]')  


class CsvReader(PydanticReader):
    def read(self, filepath: pathlib.Path, model_class: Type[TPydanticModel]) -> List[TPydanticModel]:
        """Given a valid pathlib.Path and a pydantic model class, read in a file and return a list of pydantic model instances 
        of the given type.

        Args:
            filepath (pathlib.Path): path to some file 
            model_class (TPydanticModel): A subclass of pydantic.BaseModel

        Returns:
            List[TPydanticModel]: Returns instances of the given subclass
        """
        with open(filepath, newline='') as file: 
            reader = csv.DictReader(file) # converts headers and rows to dict
            list_of_inst_models = [model_class(**dict_obj) for dict_obj in reader] 
        return list_of_inst_models 



class CsvWriter(PydanticWriter):
    def write(self, data: List[TPydanticModel], filepath: pathlib.Path) -> None:
        """Given some data as a list of PydanticModels, writes to a file. 

        Args:
            data (List[TPydanticModel]): A list of pydantic models to write 
            filepath (pathlib.Path): The filepath to write to.
        """
        with open(filepath,'w') as new_csv_file:
            headers = []
            for model_obj in data:
                for key in model_obj.dict().keys():
                    if key not in headers:
                        headers.append(key) 
            csv_writer = csv.DictWriter(new_csv_file, fieldnames=headers) 
            csv_writer.writeheader()
            list_of_py_dict = [ model_obj.dict() for model_obj in data ]
            csv_writer.writerows(list_of_py_dict)
            '''  
                - .writerow(data): writes a single row of data and returns the number of characters written. 
                - .writerows(data): writes multiple rows of data and returns None
            ''' 