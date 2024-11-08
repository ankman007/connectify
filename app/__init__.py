from fastapi import FastAPI
from app.database import create_tables, get_db_connection

def create_app():
    app = FastAPI()
    
    conn = get_db_connection()
    create_tables(conn)
    
    from app.routes.post import router as post_router
    app.include_router(post_router, prefix="/posts")
    
    from app.routes.user import router as user_router
    app.include_router(user_router)
    
    return app