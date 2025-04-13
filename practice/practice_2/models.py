# models.py
from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# Перечисление для типа расы воинов
class RaceType(str, Enum):
    director = "director"
    worker = "worker"
    junior = "junior"

# Ассоциативная сущность для связи многие-ко-многим между воином и умением
class SkillWarriorLink(SQLModel, table=True):
    warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)

# Базовая модель умения
class SkillBase(SQLModel):
    name: str
    description: Optional[str] = ""

# Модель умения с указанием таблицы и обратной связью с воинами
class Skill(SkillBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    warriors: List["Warrior"] = Relationship(back_populates="skills", link_model=SkillWarriorLink)

# Базовая модель профессии (для полноты примера, хоть в данном задании акцент на умениях)
class ProfessionBase(SQLModel):
    title: str
    description: str

class Profession(ProfessionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    warriors: List["Warrior"] = Relationship(back_populates="profession")

# Базовая модель воина (без id и ссылок), используется для входящих данных, если нужно
class WarriorBase(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")

# Основная модель воина с связями для БД
class Warrior(WarriorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Отношение к профессии; при необходимости можно вложенно возвращать данные профессии
    profession: Optional[Profession] = Relationship(back_populates="warriors")
    # Отношение многие ко многим к умениям
    skills: List[Skill] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)

# Модель для чтения (возвращения) данных о воине с вложенными объектами
class WarriorRead(WarriorBase):
    id: int
    profession: Optional[Profession] = None
    skills: List[Skill] = []
