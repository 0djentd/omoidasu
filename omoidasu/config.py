from pydantic import BaseModel


class AppConfig(BaseModel):
    debug: bool
    verbose: bool
    data_directory: str
    config_directory: str
