from fastapi import Depends
from db.database import database

session_depends = Depends(database.scoped_session_dependency)
