from fastapi import FastAPI
from app.database import create_tables, get_db_connection

def create_app():
    app = FastAPI()
    
    conn = get_db_connection()
    create_tables(conn)
    
    from app.routes.post import router as post_router
    app.include_router(post_router, prefix="/posts")
    
    from app.routes.auth import router as auth_router
    app.include_router(auth_router, prefix="/auth")
    
    from app.routes.user import router as user_router
    app.include_router(user_router, prefix="/users")
    
    return app