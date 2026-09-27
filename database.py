from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Instância global do banco de dados
db = SQLAlchemy(model_class=Base)
