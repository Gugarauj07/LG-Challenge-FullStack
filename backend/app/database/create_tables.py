from app.database.session import Base, engine
from app.models import User, Movie, Genre, Rating, Tag, Favorite

def create_tables():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso!")