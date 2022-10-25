from database.connection import create_session_factory, create_engine


class DatabaseProvider:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.session_factory = create_session_factory(self.engine)
