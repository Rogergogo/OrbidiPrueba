# ORBIDI "Map My World" FastAPI

Este proyecto es una aplicación web construida con FastAPI y SQLAlchemy, que utiliza SQLite como base de datos. A continuación se describe cómo iniciar el proyecto, construir el contenedor Docker y ejecutar pruebas.

## Requisitos

- Docker
- Docker Compose
- Python 3.8 (opcional, si no usas Docker)

## Iniciar el proyecto

- Ubicarte en la raiz del proyecto
    
    cd app


- Iniciar y construir el contenedor docker
    
    docker-compose up --build


- En el navegador copiar la siguiente url
    
    http://localhost:8000/docs#/
