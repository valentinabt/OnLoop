# OnLoop

**Una aplicación web que muestra tus 10 artistas más escuchados en Spotify** 

 [Deploy](DEPLOY.md) · [English](README-EN.md)

## Demo

### [Link](https://onloop.com.ar/)

> ⚠️ Debido a las restricciones actuales de la API de Spotify, la app está limitada a 5 usuarios de prueba. Si querés acceso, escribime para agregarte manualmente.

[ Versión Desktop ](https://github.com/user-attachments/assets/49ea0cf6-6421-469f-9f4d-d9db575ecf11) 

[Versión Mobile ](https://github.com/user-attachments/assets/159e9036-3153-471e-ae5b-9907d18d6df7)

---

### Sobre el proyecto

El proyecto integra la **API de Spotify** para mostrar los artistas más escuchados de un usuario a lo largo del tiempo.

OnLoop representó mi primer acercamiento al desarrollo web backend, donde aprendí e implementé:

- El protocolo HTTP y la arquitectura cliente-servidor
- OAuth 2.0 y flujos de autorización seguros
- Manejo de sesiones con cookies HttpOnly y protección CSRF
- Despliegue de aplicaciones en AWS EC2 con Docker
- Bases de datos NoSQL con AWS DynamoDB
- Encriptación de tokens sensibles en reposo con Fernet

### Tech Stack

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI (Python) |
| Base de datos | AWS DynamoDB |
| Infraestructura | AWS EC2 + Docker |
| Autenticación | OAuth 2.0 (Spotify) |
| Seguridad | Fernet encryption, HttpOnly cookies, CSRF state validation |
| Frontend | HTML, CSS, JavaScript (Vanilla) |

### Arquitectura

```
Browser → FastAPI (EC2) → Spotify API
                ↓
            DynamoDB
```

**Flujo de autenticación:**
1. El usuario hace click en "Login"
2. El backend genera un `state` aleatorio, lo guarda en una cookie HttpOnly y redirige a Spotify
3. Spotify redirige de vuelta al backend con un `code` y el mismo `state`
4. El backend valida que el `state` coincida (protección CSRF), intercambia el `code` por tokens y crea una sesión en DynamoDB
5. Los tokens se encriptan con Fernet antes de guardarse

**Manejo de sesiones:**
- Las sesiones tienen un TTL de 14 días desde el último refresh
- Si Spotify devuelve un 401, el frontend detecta el token vencido y llama a `/refresh` automáticamente
- Si el refresh falla, se redirige al usuario a login

### Estructura del proyecto

```
OnLoop/
├── backend/
│   ├── routers/
│   │   ├── auth.py         # /login, /callback, /logout, /refresh
│   │   ├── api.py          # /api/top-artists
│   │   └── pages.py        # /, /top-artists
│   ├── services/
│   │   ├── db.py           # DynamoDB
│   │   ├── sessions.py     # manejo de sesiones
│   │   └── spotify.py      # integración con Spotify API
│   ├── config.py
│   ├── main.py
│   └── utils.py            # encriptación
├── frontend/
│   ├── pages/
│   │   ├── login/
│   │   │   ├── login.html
│   │   │   └── login.js
│   │   └── top-artists/
│   │       ├── top-artists.html
│   │       └── top-artists.js
│   └── styles.css
├── tests/
│   ├── integration/
│   │   └── test_sessions.py
│   ├── test_callback.py
│   ├── test_login.py
│   ├── test_logout.py
│   ├── test_refresh.py
│   └── test_top_artists.py
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Endpoints


#### `GET /login`

Inicia el flujo de autenticación OAuth 2.0 con Spotify.

**Respuesta:** Redirige al usuario a la página de autorización de Spotify.

**Cookies seteadas:**

| Cookie | Descripción |
|--------|-------------|
| `oauth_state` | Token aleatorio para protección CSRF. HttpOnly, Secure. |

---

#### `GET /callback`

Endpoint de retorno del flujo OAuth. Spotify redirige aquí con el código de autorización.

**Query params:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `code` | string | Código de autorización de Spotify |
| `state` | string | State para validación CSRF |
| `error` | string | Error retornado por Spotify (opcional) |

**Respuestas:**

| Caso | Redirección |
|------|-------------|
| Éxito | `/top-artists` + cookie `session_id` seteada |
| Error de Spotify | `/?r=error` |
| Sin `code` | `/?r=error` |
| `state` inválido | `/?r=error` |
| Fallo al obtener tokens | `/?r=error` |
| Fallo al crear sesión | `/?r=error` |

**Cookies seteadas en caso de éxito:**

| Cookie | Descripción |
|--------|-------------|
| `session_id` | Identificador de sesión. HttpOnly, Secure. |

---

#### `GET /api/top-artists`

Retorna los 10 artistas más escuchados del usuario autenticado.

**Requiere cookie:** `session_id`

**Query params:**

| Parámetro | Tipo | Default | Valores posibles |
|-----------|------|---------|-----------------|
| `time_range` | string | `short_term` | `short_term`, `medium_term`, `long_term` |

**Respuesta exitosa `200`:**

```json
[
  {
    "name": "Nombre del artista",
    "image": "https://url-de-imagen.com/foto.jpg"
  }
]
```

**Respuestas de error `200`:**

| Error | Descripción |
|-------|-------------|
| `{"error": "NO_SESSION"}` | No hay cookie `session_id` o la sesión no existe |
| `{"error": "SESSION_EXPIRED"}` | El access token fue rechazado por Spotify (401) |
| `{"error": "FAILED_TO_FETCH_ARTISTS"}` | Error al comunicarse con Spotify |

---

#### `POST /refresh`

Renueva el access token usando el refresh token almacenado en sesión.

**Requiere cookie:** `session_id`

**Respuesta exitosa `200`:**

```json
{ "ok": true }
```

**Respuestas de error `200`:**

| Error | Descripción |
|-------|-------------|
| `{"error": "NO_SESSION"}` | No hay cookie `session_id` o no hay refresh token asociado |
| `{"error": "FAILED_TO_REFRESH"}` | Spotify rechazó el refresh token o falló la actualización en DynamoDB |

---

#### `GET /logout`

Elimina la sesión del usuario y borra la cookie `session_id`.

**Requiere cookie:** `session_id`

**Respuestas:**

| Caso | Redirección |
|------|-------------|
| Éxito | `/` + cookie `session_id` eliminada |
| Sin `session_id` | `/?r=error` |
| Fallo al eliminar sesión | `/?r=error` |

---

### Parámetros de query en redirecciones

Cuando el frontend recibe una redirección con `?r=`, muestra un toast con el mensaje correspondiente:

| Valor | Mensaje |
|-------|---------|
| `no_session` | "Por favor, inicie sesión" |
| `session_expired` | "Tu sesión ha expirado, por favor inicie sesión nuevamente" |
| `fetch_error` | "No se pudieron cargar tus artistas, intentá nuevamente" |
| `error` | "Algo salió mal, intentá nuevamente" |

---

### Limitaciones de la API de Spotify

Debido a las políticas actuales de Spotify, la aplicación se encuentra en modo de desarrollo, lo que limita el acceso a un grupo reducido de usuarios de prueba. Dadas las estrictas condiciones requeridas para pasar a producción, el proyecto se mantiene como una prueba de concepto completamente funcional y desplegada en [onloop.com.ar](https://onloop.com.ar).

*Made by [valensancho](https://github.com/valensancho)*
