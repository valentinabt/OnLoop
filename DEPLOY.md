# Guía de Deploy — OnLoop

[English](#-deploy-guide--onloop)

---

## Índice

1. [Configurar Spotify Developer Dashboard](#1-configurar-spotify-developer-dashboard)
2. [Crear la tabla en DynamoDB](#2-crear-la-tabla-en-dynamodb)
3. [Generar la Fernet Key](#3-generar-la-fernet-key)
4. [Configurar variables de entorno](#4-configurar-variables-de-entorno)
5. [Correr con Docker](#5-correr-con-docker)
6. [Correr los tests](#6-correr-los-tests)

---

## 1. Configurar Spotify Developer Dashboard

1. Entrá a [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Hacé click en **Create app**
3. Completá el nombre y descripción
4. En **Redirect URIs** agregá: `http://127.0.0.1:8000/callback`
5. En **APIs used** seleccioná **Web API**
6. Guardá y abrí la app — copiá el **Client ID** y el **Client Secret**

>  Spotify limita las apps en modo Development a 5 usuarios de prueba. Para agregar usuarios, andá a **User Management** dentro de tu app en el dashboard.

---

## 2. Crear la tabla en DynamoDB

1. Entrá a la consola de AWS y abrí **DynamoDB**
2. Hacé click en **Create table**
3. Configurá:
   - **Table name:** el nombre que quieras (ej. `sessions`)
   - **Partition key:** `session_id` (tipo `String`)
4. En **Table settings** dejá **Default settings**
5. Creá la tabla
6. Una vez creada, andá a la tabla → **Additional settings** → **Time to Live (TTL)**
7. Activá TTL con el atributo `ttl`

---

## 3. Generar la Fernet Key

La Fernet key se usa para encriptar los tokens de Spotify antes de guardarlos en DynamoDB.

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copiá el resultado — lo vas a usar como `ENCRYPTION_KEY` en el paso siguiente.

> Si no tenés Python con la librería `cryptography` instalada, podés generarla después de levantar Docker (ver paso 5).

---

## 4. Configurar variables de entorno

Creá un archivo `.env` en la raíz del proyecto:

```env
CLIENT_ID=tu_spotify_client_id
CLIENT_SECRET=tu_spotify_client_secret
REDIRECT_URI=http://127.0.0.1:8000/callback
FRONTEND_URL=http://127.0.0.1:8000
ENCRYPTION_KEY=tu_fernet_key
DYNAMODB_TABLE_NAME=sessions
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-2
```

---

## 5. Correr con Docker

### Requisitos
- Docker 20.10 o superior 

### Pasos

```bash
git clone https://github.com/valensancho/OnLoop
cd OnLoop
docker compose up --build
```

La app queda disponible en `http://127.0.0.1:8000`.

Para correrla en background:

```bash
docker compose up -d --build
```

Para detenerla:

```bash
docker compose down
```

> Si necesitás generar la Fernet Key desde el contenedor:
> ```bash
> docker exec -it onloop_backend_1 python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
> ```
> Copiá el resultado, actualizá el `.env` y rebuildeá con `docker compose up -d --build`.

---

## 6. Correr los tests

### Tests unitarios

```bash
docker exec -it onloop_backend_1 pytest tests/
```

### Tests de integración

Los tests de integración corren contra una tabla de DynamoDB real. Creá una tabla de test siguiendo los mismos pasos de la [sección 2](#2-crear-la-tabla-en-dynamodb) con un nombre distinto (ej. `sessions-test`).

```bash
docker exec -it \
  -e DYNAMODB_TABLE_NAME=sessions-test \
  onloop_backend_1 pytest tests/integration/
```

### Correr todos los tests

```bash
docker exec -it \
  -e DYNAMODB_TABLE_NAME=sessions-test \
  onloop_backend_1 pytest tests/
```

---
---

#  Deploy Guide — OnLoop

[Español](#-guía-de-deploy--onloop)

---

## Index

1. [Set up Spotify Developer Dashboard](#1-set-up-spotify-developer-dashboard)
2. [Create the DynamoDB table](#2-create-the-dynamodb-table)
3. [Generate the Fernet Key](#3-generate-the-fernet-key)
4. [Configure environment variables](#4-configure-environment-variables)
5. [Run with Docker](#5-run-with-docker)
6. [Run the tests](#6-run-the-tests)

---

## 1. Set up Spotify Developer Dashboard

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click **Create app**
3. Fill in the name and description
4. Under **Redirect URIs** add: `http://127.0.0.1:8000/callback`
5. Under **APIs used** select **Web API**
6. Save and open the app — copy the **Client ID** and **Client Secret**

>  Spotify limits apps in Development mode to 5 test users. To add users, go to **User Management** inside your app on the dashboard.

---

## 2. Create the DynamoDB table

1. Go to the AWS console and open **DynamoDB**
2. Click **Create table**
3. Configure:
   - **Table name:** anything you want (e.g. `sessions`)
   - **Partition key:** `session_id` (type `String`)
4. Under **Table settings** leave **Default settings**
5. Create the table
6. Once created, go to the table → **Additional settings** → **Time to Live (TTL)**
7. Enable TTL with the attribute `ttl`

---

## 3. Generate the Fernet Key

The Fernet key is used to encrypt Spotify tokens before storing them in DynamoDB.

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the result — you'll use it as `ENCRYPTION_KEY` in the next step.

> If you don't have Python with the `cryptography` library installed, you can generate it after starting Docker (see step 5).

---

## 4. Configure environment variables

Create a `.env` file in the project root:

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://127.0.0.1:8000/callback
FRONTEND_URL=http://127.0.0.1:8000
ENCRYPTION_KEY=your_fernet_key
DYNAMODB_TABLE_NAME=sessions
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-2
```

---

## 5. Run with Docker

### Requirements
- Docker 20.10 or higher 

### Steps

```bash
git clone https://github.com/valensancho/OnLoop
cd OnLoop
docker compose up --build
```

The app will be available at `http://127.0.0.1:8000`.

To run in the background:

```bash
docker compose up -d --build
```

To stop it:

```bash
docker compose down
```

> If you need to generate the Fernet Key from the container:
> ```bash
> docker exec -it onloop_backend_1 python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
> ```
> Copy the result, update the `.env`, and rebuild with `docker compose up -d --build`.

---

## 6. Run the tests

### Unit tests

```bash
docker exec -it onloop_backend_1 pytest tests/
```

### Integration tests

Integration tests run against a real DynamoDB table. Create a test table following the same steps in [section 2](#2-create-the-dynamodb-table) with a different name (e.g. `sessions-test`).

```bash
docker exec -it \
  -e DYNAMODB_TABLE_NAME=sessions-test \
  onloop_backend_1 pytest tests/integration/
```

### Run all tests

```bash
docker exec -it \
  -e DYNAMODB_TABLE_NAME=sessions-test \
  onloop_backend_1 pytest tests/
```
