import sqlalchemy


class DatabaseClient:

    def __init__(self, database_uri: str):
        self._database_uri = database_uri
        self._db = sqlalchemy.create_engine(self._database_uri)

    def __call__(self, *args, **kwargs):
        return self._db
