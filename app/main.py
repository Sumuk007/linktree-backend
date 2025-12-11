from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import profiles, redirects

app = FastAPI(title="Linktree Clone API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://linktree-backend-production-2969.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(profiles.router)
app.include_router(redirects.router)

@app.get("/")
def root():
    return {"message": "Linktree Clone API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
