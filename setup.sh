#!/bin/bash
# --------------------------------------------------
# SCRIPT DE PREPARACIÓN Y EJECUCIÓN (Linux/Mac)
# Proyecto: GluteOS
# Asignatura: Ingeniería de Software 1
# --------------------------------------------------

echo "Iniciando script de configuración..."

# --- Bloque 0: Variables de entorno ---
if [ ! -f Project/.env ]; then
  echo "Creando Project/.env a partir de Project/.env.example (cambia los valores antes de usarlo en serio)..."
  cp Project/.env.example Project/.env
fi

# --- Bloque 1: Instalación de Dependencias ---
echo "Instalando dependencias (pip3 install -r project/requirements.txt)..."
pip3 install -r project/requirements.txt

# --- Bloque 2: Preparación de la Base de Datos (Migraciones) ---
echo "Aplicando migraciones de la BD (python3 project/manage.py migrate)..."
python3 project/manage.py migrate

# --- Bloque 3: Ejecución de Pruebas Básicas ---
echo "Ejecutando pruebas (python3 project/manage.py test)..."
python3 project/manage.py test

# --- Bloque 4: Ejecución Inicial ---
echo "Iniciando la aplicación (python3 project/manage.py runserver)..."
python3 project/manage.py runserver

echo "Script finalizado."