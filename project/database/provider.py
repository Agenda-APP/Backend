from database.connection import create_database_engine, create_session_factory


class DatabaseProvider:
    def __init__(self, db_url: str):
        self.engine = create_database_engine(db_url)
        self.session_factory = create_session_factory(self.engine)
