# Workshop 02 - Sistemas Operativos: Servidores

## Descripcion

API REST creada con **FastAPI** y **SQLite** que permite leer y escribir datos en una tabla `items` con las columnas: `id`, `name`, `price`, `created_at`.

Cada endpoint cuenta con su propia clase de validacion (heredando de `BaseModel` de Pydantic) para los datos de request y response.

## Estructura del proyecto

```
OS-Workshop02/
├── api.py          # Endpoints POST /items y GET /items
├── models.py       # Clases Pydantic (BaseModel) para validacion
├── database.py     # Capa de base de datos SQLite
├── items.db        # Base de datos SQLite (se crea automaticamente)
├── items-api.service  # Archivo systemd .service
└── README.md
```

## Evidencia - API funcionando (Swagger UI)

![Backend corriendo en localhost](images/backend%20corriendo%20en%20localhost.png)

No puedo mostrarlo funcionando desde un servicio ya que no estoy en WSL sino en MacOS.Aquí se usaría la carpeta launchd y un archivo .plist (Lo intente varias. veces y al final no funcionó TwT)

## Requisitos

```bash
pip install fastapi uvicorn pydantic
```

Estas son las librerias que nos permiten que el backend nos funcione.

## Como ejecutar la API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

La API estara disponible en `http://localhost:8000`.

La documentacion interactiva (Swagger UI) esta en `http://localhost:8000/docs`


## Endpoints

### POST /items

Agrega uno o mas items a la base de datos.

**Request body:**

```json
{
  "items": [
    {"name": "Laptop", "price": 999.99},
    {"name": "Mouse", "price": 25.50}
  ]
}
```

**Response:**

```json
{
  "items": [
    {"id": 1, "name": "Laptop", "price": 999.99, "created_at": "2026-03-29T12:00:00"},
    {"id": 2, "name": "Mouse", "price": 25.50, "created_at": "2026-03-29T12:00:00"}
  ]
}
```

### GET /items

Lee los datos de la tabla. Soporta paginacion con `limit` y `offset`.

```
GET /items
GET /items?limit=10&offset=0
```

**Response:**

```json
{
  "items": [
    {"id": 1, "name": "Laptop", "price": 999.99, "created_at": "2026-03-29T12:00:00"},
    {"id": 2, "name": "Mouse", "price": 25.50, "created_at": "2026-03-29T12:00:00"}
  ]
}
```

## Clases de validacion (Pydantic BaseModel)


| Clase              | Tipo          | Descripcion                       |
| ------------------ | ------------- | --------------------------------- |
| `ItemBase`         | Request       | Valida name (str) y price (float) |
| `ItemSchema`       | Response      | Item completo con id y created_at |
| `PostItemRequest`  | Request POST  | Lista de ItemBase                 |
| `PostItemResponse` | Response POST | Lista de ItemSchema               |
| `GetItemsRequest`  | Request GET   | Parametros limit y offset         |
| `GetItemsResponse` | Response GET  | Lista de ItemSchema               |


## Archivo .service (systemd)

El archivo `items-api.service` permite que la API se inicie automaticamente con el sistema operativo.  
(No se muestra como lo requiere ya que estoy en MacOS y es diferente)

### Instalacion del servicio (Linux/WSL)

```bash
# Copiar el archivo .service a systemd
sudo cp items-api.service /etc/systemd/system/

# Recargar la configuracion de systemd
sudo systemctl daemon-reload

# Habilitar el servicio para que inicie con el sistema
sudo systemctl enable items-api.service

# Iniciar el servicio
sudo systemctl start items-api.service

# Verificar el estado
sudo systemctl status items-api.service
```

> **Nota:** Editar el archivo `.service` para ajustar las rutas (`WorkingDirectory` y `ExecStart`) segun su sistema.

## NGROK - Exponer la API publicamente

### Que es NGROK?

NGROK es una herramienta que crea tuneles seguros desde internet hacia tu computador local. Permite exponer un servidor local (como esta API) para que cualquier persona pueda acceder a el desde cualquier lugar del mundo a traves de una URL publica.

### Instalacion

**MacOS (con Homebrew):**

```bash
brew install ngrok
```


### Configuracion

1. Crear una cuenta en [ngrok.com](https://ngrok.com)
2. Obtener el authtoken desde el dashboard
3. Configurar el token:

```bash
ngrok config add-authtoken <TU_TOKEN>
```

### Uso

Con la API corriendo en el puerto 8000:

```bash
ngrok http 8000
```

NGROK mostrara una URL publica (ej: `https://xxxx-xxxx.ngrok-free.app`) que redirige al servidor local. Cualquier persona puede usar esa URL para acceder a la API.

### Evidencia - NGROK funcionando

![Curl desde terminal](images/Curl%20desde%20terminal.png)

![Ngrok trabajando](images/Ngrok%funcionando%en%la%terminal.png)

![Request desde navegador](images/Request%20desde%20navegador%20.png)

### Ejemplo de uso con la URL publica

```bash
# POST - Agregar items
curl -X POST https://xxxx-xxxx.ngrok-free.app/items \
  -H "Content-Type: application/json" \
  -d '{"items": [{"name": "Teclado", "price": 45.00}]}'

# GET - Leer items
curl https://xxxx-xxxx.ngrok-free.app/items
```

---

## Servicio adicional: n8n (Workflow Automation)

### Que es n8n?

n8n es una herramienta de automatizacion de flujos de trabajo (similar a Zapier) que permite conectar diferentes servicios y APIs de forma visual. Es open-source y se puede desplegar localmente. Principalmente elegí n8n ya que en mi trabajo tengo serivcios activamente corriendo en n8n que interactuan con webhooks, intleigencia artifical y peticiones a otros sitios web.

### Instalacion con Docker

```bash
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

n8n estara disponible en `http://localhost:5678`.

### Archivo .service para n8n

El archivo `n8n.service` permite que n8n se inicie automaticamente con el sistema en Linux/WSL.

```bash
sudo cp n8n.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable n8n.service
sudo systemctl start n8n.service
```

### Exponer n8n con NGROK

```bash
ngrok http 5678
```

### Evidencia - n8n funcionando con NGROK

![n8n corriendo local](images/n8n%20Corriendo%20local.png)

![n8n desplegado en Docker](images/imagen%20de%20n8n%20desplegado%20en%20docker.png)

![n8n con URL publica de ngrok](images/n8n%20con%20la%20url%20publica%20de%20ngrok.png)