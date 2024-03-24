from fastapi import FastAPI, HTTPException, Query, status
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Base, VMSchema, ServerSchema, ReplacementSchema
from models import VMModel, ServerModel, ReplacementModel
from typing import List

engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_severs(db, size):
    servers = db.query(ServerSchema).filter(ServerSchema.status == "up").all()
    servers_list = []
    for server in servers:
        server_model = ServerModel.from_orm(server)
        if server_model.memory_allow >= size:
            servers_list.append(server_model)
    return servers_list

@app.post("/create/", status_code=status.HTTP_201_CREATED)
def create_article(vm_create: VMModel):
    db = SessionLocal()
    uniq = db.query(VMSchema).filter(VMSchema.id == vm_create.id).first()
    if uniq != None:
        db.close()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="VM with this id is already created")
    
    #получаем серверы с доступными ресурсами по памяти
    servers = get_severs(db, vm_create.size)
    if len(servers) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"result": "NOT_OK"})
    db.close()
    #обновляем информацию о сервере
    db = SessionLocal()
    db_server = db.query(ServerSchema).filter(ServerSchema.id == servers[0].id).first()
    
    setattr(db_server, "memory_allow", db_server.memory_allow-vm_create.size)

    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    db.close()

    #создаём ВМ
    db = SessionLocal()
    db_vm_create = VMSchema(**vm_create.dict())
    db.add(db_vm_create)
    db.commit()
    db.refresh(db_vm_create)
    db.close()

    # #создаём связь между сервером и ВМ
    # db = SessionLocal()
    # print(db_vm_create.id, db_server.id)

    # new_replacement = ReplacementModel(id_vm = db_vm_create.id, id_server = db_server.id)
    
    
    # # new_replacement.id_server = db_server.id
    # db_replacement = ReplacementSchema(**new_replacement.dict())
    # db.add(db_replacement)
    # db.commit()
    # db.refresh(db_replacement)
    # db.close()
    return {"result": "OK", "host_id": db_server.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9024)
