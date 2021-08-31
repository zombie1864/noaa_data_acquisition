'''  
One of the nice things about python is that a class is in and of itself an object. We can leverage 
this to create modularity in our library code. 
This method of API building is an example of what's called the Interface Segregation Principle. Basically 
this states that you should strive to create small abstract interfaces with very narrow functionality to increase 
flexibility. 
'''


import pydantic
import abc 
import pathlib
import csv 
from typing import List, Type, TypeVar


TPydanticModel = TypeVar('TPydanticModel', bound=pydantic.BaseModel) #declares a custom type to use with our interface


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



class JsonWriter(PydanticWriter):
    def write(self, data: List[TPydanticModel], filepath: pathlib.Path) -> None:
        """Given a list of PydanticModels, writes to a json file. 

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
        """Given a valid pathlib.Path and a pydantic model class, read in a file and return a list of pydantic model instances of the given type.

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
