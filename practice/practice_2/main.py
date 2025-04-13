# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session
from typing import List
from models import Warrior, WarriorRead, Skill, Profession
from connection import engine, init_db, get_session

app = FastAPI()

# При старте приложения создаются таблицы в БД
@app.on_event("startup")
def on_startup():
    init_db()

# ---------------------------
# ЭНДПОИНТЫ ДЛЯ РАБОТЫ С ВОИНАМИ
# ---------------------------

# Создание нового воина. В теле запроса можно передать также список умений,
# если они уже существуют (или можно передать пустой список).
@app.post("/warrior", response_model=WarriorRead)
def create_warrior(warrior: Warrior, session: Session = Depends(get_session)):
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return warrior

# Получение списка воинов с вложенными умениями и профессией
@app.get("/warriors", response_model=List[WarriorRead])
def get_warriors(session: Session = Depends(get_session)):
    warriors = session.exec(select(Warrior)).all()
    return warriors

# Получение воина по id с вложенными умениями
@app.get("/warrior/{warrior_id}", response_model=WarriorRead)
def get_warrior(warrior_id: int, session: Session = Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior

# Частичное обновление воина (например, изменение имени или уровня)
@app.patch("/warrior/{warrior_id}", response_model=WarriorRead)
def update_warrior(warrior_id: int, warrior_data: Warrior, session: Session = Depends(get_session)):
    warrior_db = session.get(Warrior, warrior_id)
    if not warrior_db:
        raise HTTPException(status_code=404, detail="Warrior not found")
    update_data = warrior_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(warrior_db, key, value)
    session.add(warrior_db)
    session.commit()
    session.refresh(warrior_db)
    return warrior_db

# Удаление воина по id
@app.delete("/warrior/{warrior_id}")
def delete_warrior(warrior_id: int, session: Session = Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}

# Привязка (добавление) умения к воину по id
@app.post("/warrior/{warrior_id}/add_skill/{skill_id}", response_model=WarriorRead)
def add_skill_to_warrior(warrior_id: int, skill_id: int, session: Session = Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    # Если умение уже не привязано, добавляем его
    if skill not in warrior.skills:
        warrior.skills.append(skill)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return warrior

# ---------------------------
# ЭНДПОИНТЫ ДЛЯ РАБОТЫ С УМЕНИЯМИ
# ---------------------------

# Создание нового умения
@app.post("/skill", response_model=Skill)
def create_skill(skill: Skill, session: Session = Depends(get_session)):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

# Получение списка умений
@app.get("/skills", response_model=List[Skill])
def get_skills(session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills

# Получение умения по id
@app.get("/skill/{skill_id}", response_model=Skill)
def get_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Обновление умения (частичное обновление)
@app.patch("/skill/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill_data: Skill, session: Session = Depends(get_session)):
    skill_db = session.get(Skill, skill_id)
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    update_data = skill_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(skill_db, key, value)
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)
    return skill_db

# Удаление умения
@app.delete("/skill/{skill_id}")
def delete_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}
