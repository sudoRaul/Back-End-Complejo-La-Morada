import os

DB_HOST = "localhost"
DB_NAME = "complejo_deportivo"
DB_USER = "root"  # Cambiar si tienes una contraseña
DB_PASSWORD = ""  # Pon tu contraseña si la has establecido

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
