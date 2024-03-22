
# Reto: Procesamiento de Datos

Introducción a FastApi, pydantic y OAuth

## Descripción:

- Realizar un modelo de datos que se ajuste a un parque eólico, en el que hay 10 generadores y un concentrador, es necesario que con una probabilidad N vengan datos erróneos.
  
- El concentrador se implementa con FastAPI que sea capaz de validar los datos.
  
- Realizar algún tipo de agregación (e.j, media de producción del parque, agregados minutales)
  
- Los generadores deben ser programas individuales que generan datos sintéticos diferentes.
  
- Extra: Seguridad en la comunicación.

## Estructura 🏗️

![image](https://github.com/jdecruzdeusto/Reto-MQTT-SEGURO/assets/125390240/dd2617ed-8ace-499b-a9b4-88c15a177a0d)

## Ejecución 🚀

0. REQUERIMIENTOS

Instalar los paquetes necesarios:
```bash
pip install fastapi uvicorn pydantic httpx python-multipart
```

1. Ejecutar el comando para iniciar una aplicación FastAPI (o cualquier otra aplicación ASGI) utilizando Uvicorn:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

2. Abrir otra terminal bash y ejecutar main.py:
```bash
python3 main.py
```
3. Abrir Swagger UI utilizando la siguiente URL:
```url
http://localhost:8000/docs
```
4. Autenticación (Clickar el en botón y meter usuario "user" y contraseña "password"):
![Captura de pantalla 2024-03-22 120851](https://github.com/jdecruzdeusto/procesamientoDeDatos/assets/125390240/607702a1-1ed1-4a31-bc0a-9542256655a7)

## Pasos seguidos para realizar el reto 🚶

1. Leer y entender qué son y cómo funcionan FastApi y Pydantic
   
2. Definir la clase Generador con sus respectivos atributos y con valores generados mediante la función random()
   
3. Configurar FastApi y crear los métodos POST y GET necesarios
   
4. Implemntar la validación mediante Pydantic para que no se puedan introducir datos < 0
   
5. Añadir agregaciones de datos sobre la media de los valores y crear los métodos GET y POST

6. Implementar la validación mediante OAuth por medio de una token jwt

## Posibles vías de mejora 📈
- Implementar persistencia de datos

- Meter más datos, tanto más tipos de datos como clases y atributos

- Crear una interfaz de usuario real, en vez de usar Swagger UI

- Prometheus y Grafana para monitoreo

## Alternativas posibles 🔜
- Explorar otros lenguajes de programación, como utilizar C# para la estructura y ASP.net Core para la Api

- Certificados de seguridad

## Problemas / Retos encontrados ❗
- Implementar la validación correctamente

- Nunca había usado seguridad OAuth
