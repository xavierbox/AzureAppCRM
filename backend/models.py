
from typing import List, Optional,Tuple,Any, Literal
from pydantic import Field, BaseModel
from datetime import datetime, timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
import time 

class UploadSimulatorFilesModel( BaseModel ):

    simulation_name: str = Field( description='unique simulation id')
    simulator_name:  Literal['crm','ix'] = Field(default='crm', 
                                                 description='unique simulation id')
    sas : Optional[str] = Field( default=None, description='SAS token received from backend')

__all__=['UploadSimulatorFilesModel']





if __name__ == '__main__':
    print('main')