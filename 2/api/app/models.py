from pydantic import BaseModel, validator


class VMModel(BaseModel):
    id: int
    size: int
    task: str
    
    @validator("size")
    @classmethod
    def validate_size(cls, value):
        flag = (value & (value-1) == 0) and value > 0
        if not flag:
            raise ValueError("Size must be from 1 to 128 and power of 2")
        return value

class ServerModel(BaseModel):
    id: int
    cpu_all: int
    memory_all: int
    cpu_allow: int
    memory_allow: int
    status: str

    def __init__(self, id, cpu_all, memory_all, cpu_allow, memory_allow, status):
        self.id = id
        self.cpu_all = cpu_all
        self.memory_all = memory_all
        self.cpu_allow = memory_allow
        self.cpu_all = cpu_allow
        self.status = status  
    # @validator("status")
    # @classmethod
    # def validate_status(cls, value):
    #     if value != "up" or value != "down":
    #         raise ValueError("Status must be up or down")
    #     return value
    
    class Config:
        orm_mode = True
        from_attributes = True

    
class ReplacementModel(BaseModel):
    id_vm: int
    id_server: int