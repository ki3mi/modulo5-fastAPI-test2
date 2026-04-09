# main.py - Punto de entrada de la aplicacion FastAPI
# Aqui se configura el servidor y se registran las rutas
# Equivalente a app.js en Express o Program.cs en ASP.NET
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import prestamos
app = FastAPI(
    title="Portal Mi Banco -- Modulo Prestamos",
    version="1.0.0",
    description="API del simulador de prestamos con documentacion automatica"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(prestamos.router, prefix="/api/prestamos", tags=["Prestamos"])
# Iniciar:  uvicorn main:app --reload
# API en:   http://localhost:8000
# DOCS en:  http://localhost:8000/docs