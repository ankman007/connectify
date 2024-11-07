from fastapi import FastAPI

def create_app():
    app = FastAPI()
    
    from app.routes.post import router as post_router
    app.include_router(post_router, prefix="/posts")
    
    # from app.routes.user import router as user_router
    # app.include_router(user_router, prefix="/users")
    
    return app