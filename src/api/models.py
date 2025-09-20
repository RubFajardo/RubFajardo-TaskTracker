from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

db = SQLAlchemy()

api = Blueprint('api', __name__)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    tasks: Mapped[List["Task"]] = relationship(back_populates="author")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }
    
    def get_all_tasks(self):
        all_tasks = []
        for task in self.tasks:
            all_tasks.append(task.serialize())
        return all_tasks   
    

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="tasks")



    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done
        }
