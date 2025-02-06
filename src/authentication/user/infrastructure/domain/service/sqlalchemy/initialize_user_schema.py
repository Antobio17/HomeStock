import os
import uuid
import glob
from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy import create_engine, text # type: ignore
from sqlalchemy.schema import CreateSchema # type: ignore

@dataclass
class InitializeUserSchema:
    __schema_name: str
    __email: str
    __database_writer_url: str = os.getenv('DATABASE_WRITER_URL')
    
    def execute(self):
        engine = create_engine(self.__database_writer_url)
        sql = """
        SELECT SCHEMA_NAME 
        FROM INFORMATION_SCHEMA.SCHEMATA 
        WHERE SCHEMA_NAME = :schema_name
        """
        with engine.connect() as connection:
            result = connection.execute(text(sql), {'schema_name': self.__schema_name})
            schema_exists = result.fetchone() 
            if schema_exists is not None:
                return
            
            connection.execute(CreateSchema(self.__schema_name))
        engine.dispose()
        
        engine = create_engine(self.__database_writer_url + self.__schema_name)
        sql = """
        INSERT INTO `user` (`id`, `email`, `sub`, `created_at`) 
        VALUES (:uuid, :email, :sub, :created_at)
        """
        with engine.connect() as connection:
            pattern = 'src/*/*/infrastructure/domain/model/sqlalchemy/migration/*.sql'
            for filepath in glob.glob(pattern):
                with open(filepath, 'r') as file:
                    connection.execute(text(file.read()))
            
            connection.execute(text(sql), {
                'uuid': uuid.uuid4(),
                'email': self.__email,
                'sub': self.__schema_name,
                'created_at': datetime.now(timezone.utc).isoformat()
            })    
            connection.commit()
            
        engine.dispose()