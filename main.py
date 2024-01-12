from fastapi import FastAPI, Depends, Body, status
from database.database import *
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, FileResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(title='NEW PROJECT')

def get_user(id: int):
    return db.query(Person).filter(Person.id == id).first()

def get_db():
    try:
        print('a')
        yield db
    finally:
        db.close()

@app.get('/')
def main():
    return FileResponse('public/index.html')

@app.get('/api/users')
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()

@app.get('/api/users/{id}', description='Поиск человека по айди')
def get_person(id: int, db: Session = Depends(get_db)):
    person = get_user(id)
    if person is None:
        return JSONResponse(content={'message': 'Пользователь не найден'}, status_code=status.HTTP_404_NOT_FOUND)
    return person

@app.post('/api/users')
def create_person(data = Body(), db: Session = Depends(get_db)):
    person = Person(name=data['name'], age=data['age'])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person



@app.put('/api/users')
def edit_person(data=Body(), db: Session = Depends(get_db)):
    person = get_user(id)

    if person is None:
        return JSONResponse(content={'message': 'Пользователь не найден'}, status_code=status.HTTP_404_NOT_FOUND)
    person.age = data['age']
    person.name = data['name']
    db.commit()
    db.refresh(person)
    return person

@app.delete('/api/users/{id}')
def delete_person(id: int, db: Session = Depends(get_db)):
    person = get_user(id)

    if person is None:
        return JSONResponse(content={'message': 'Такого пользователя нет!'}, status_code=status.HTTP_404_NOT_FOUND)
    db.delete(person)
    db.commit()
    return person
    
