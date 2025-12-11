from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import profiles, redirects

app = FastAPI(title="Linktree Clone API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",  # Allow all Vercel preview deployments
        "https://your-frontend-domain.vercel.app"  # Replace with your actual domain
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
