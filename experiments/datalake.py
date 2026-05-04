from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional
from pathlib import Path 
ACCOUNT_NAME = "launchedstorage"
FILESYSTEM_NAME = "launcherdata"


from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from azure.storage.filedatalake import DataLakeServiceClient


class StorageConfig(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    app_folder_name: str = Field(
        description="Root folder for the app",
        default = "wf"
    )

    projects_folder_name: str = Field(
        default="projects",
        description="Root folder for projects: {app_folder}/{projects_folder}"
    )

    data_folder_name: str = Field(
        default="data",
        description="Root folder for datasets inside each project"
    )



    credential: Optional[Any] = Field(
        default=None,
        exclude = True  
    )

    account: Optional[Any] = Field(
        default=None
    )

    file_system_name: str = Field(
        default="appdata",
        description="Azure Data Lake filesystem name"
    )




    @property
    def account_url(self) -> str:
        return f"https://{self.account}.dfs.core.windows.net"

    #@property
    #def root_path(self) -> str:
    #    return f"{self.app_folder}/{self.projects_folder}"


class Storage(BaseModel):
    """
    Hierarchical Azure Storage manager.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: StorageConfig
 
    def _get_handler(self):
        """
        Returns DataLake filesystem client.
        """
        service_client = DataLakeServiceClient(
            account_url=self.config.account_url,
            credential=self.config.credential
        )

        return service_client.get_file_system_client(
            self.config.file_system_name
        )

    def create_project( self, project_name ):

        handler = self._get_handler()

        handler.create_file_system() 

        return 
        project_path = Path(f"{self.config.app_folder_name}/{self.config.projects_folder_name}")

        new_path = f"Filesystem '{FILESYSTEM_NAME}' created successfully."

        fs_client = handler.get_directory_client("new_path")
        fs_client.create_directory()
        print(f"Dir '{new_path}' created successfully.")




config = StorageConfig(app_folder_name="wf",
                       credential = DefaultAzureCredential(),
                       account=ACCOUNT_NAME)
storage = Storage( config = config )
#storage.create_project("aaa")
#
#print( storage.model_dump_json( indent = 3 ))



account_url = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"
credential = DefaultAzureCredential()
service_client = DataLakeServiceClient(
    account_url=account_url,
    credential=credential
)

fs_client = service_client.get_file_system_client("wfapp")
try:
    fs_client.create_file_system()
    print(f"Filesystem '{FILESYSTEM_NAME}' created successfully.")


    fs_client.create_directory("projects")
    fs_client.create_directory("projects/project1")
    fs_client.create_directory("projects/project1/data")
    fs_client.create_directory("projects/project1/studies")
    fs_client.create_directory("projects/project1/temporal")
except:
    pass 

dir = fs_client.get_directory_client("projects/project1/studies")

import json 
import datetime 
d = datetime.datetime.now().strftime
data = {'creation__time':d }

content = json.dumps( data ) 
file = dir.get_file_client("config.json")
file.create_file()
file.upload_data( content )
#file.append_data( data = content, offset = 0 )
#file.flush_data( len(content)) 



