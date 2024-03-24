from sqlalchemy import Column, Integer, String, ForeignKey, func

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ServerSchema(Base):
    __tablename__ = 'Server'
    id = Column(Integer, primary_key=True, index=True)
    cpu_all = Column(Integer)
    memory_all = Column(Integer)
    cpu_allow = Column(Integer)
    memory_allow = Column(Integer)
    status = Column(String)
    

class VMSchema(Base):
    __tablename__ = 'VM'
    id = Column(Integer, primary_key=True, index=True)
    size = Column(Integer)
    task = Column(String)

class ReplacementSchema(Base):
    __tablename__ = 'Replacement'
    id = Column(Integer, primary_key=True, index=True)
    vm_id = Column(Integer, ForeignKey('VM.id'))
    server_id = Column(Integer, ForeignKey('Server.id'))
