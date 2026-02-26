# Markdown to PDF

Microservicio dockerizado en Python para convertir archivos Markdown a PDF. Disponible como interfaz web y API REST.

## Características

- **Interfaz web** intuitiva con textarea
- **API REST** para integración con otros sistemas
- Conversión de Markdown a PDF en tiempo real
- Soporte completo de sintaxis Markdown:
  - Encabezados (H1-H6)
  - Negrita, cursiva y tachado
  - Listas ordenadas y desordenadas
  - Enlaces e imágenes
  - Bloques de código con sintaxis
  - Tablas
  - Citas
  - Y más...
- Diseño PDF profesional con estilos CSS personalizados
- Dockerizado para fácil despliegue
- Descarga automática del PDF generado
- **Autenticación con API Key** para proteger endpoints

## Seguridad

El microservicio incluye un **sistema de autenticación con API Key OBLIGATORIA** para proteger todos los endpoints.

### ⚠️ IMPORTANTE: API Key Obligatoria

**La API Key es SIEMPRE requerida** para acceder tanto a la interfaz web como a la API REST. Sin ella, la aplicación no funcionará.

### Configuración de API Key

**Configuración inicial (OBLIGATORIA):**

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` y configura tu API Key:
```env
API_KEY=tu-api-key-super-secreta-aqui
FLASK_ENV=production
FLASK_DEBUG=False

# Rate Limiting (opcional - ajusta según necesidades)
RATE_LIMIT_API_CONVERT=10 per minute
# Usa 'unlimited' para sin límite
```

3. Levanta el servicio:
```bash
docker-compose up
```

O configura directamente en `docker-compose.yml`:
```yaml
environment:
  - API_KEY=tu-api-key-super-secreta-aqui
```

**Recomendaciones de seguridad:**
- Genera una API Key fuerte: `openssl rand -hex 32`
- Nunca compartas tu API Key públicamente
- Rota la API Key periódicamente
- Guarda el archivo `.env` en un lugar seguro (nunca lo subas a Git)

### Uso con API Key

Incluye el header `X-API-Key` en tus peticiones al endpoint `/api/convert`:

```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key-super-secreta-aqui" \
  -d '{"markdown": "# Hola"}' \
  --output documento.pdf
```

**Notas importantes sobre endpoints:**
- **`/`** - Interfaz web: **Requiere API Key** (campo en el formulario)
- **`/convert`** - Conversión web: **Requiere API Key** (enviada desde formulario)
- **`/api/convert`** - API REST: **Requiere API Key** (header X-API-Key)
- **`/api/health`** - Healthcheck: **Público** (no requiere API Key)

**Protecciones de seguridad:**
- ✅ Autenticación obligatoria con API Key
- ✅ Rate limiting configurable (10 peticiones/minuto por defecto)
- ✅ Validación de entrada
- ✅ Protección contra fuerza bruta

### Configuración de Rate Limiting

El rate limiting es **completamente configurable** desde el archivo `.env`:

**Valores disponibles por endpoint:**
```env
# Interfaz web
RATE_LIMIT_WEB_INDEX=20 per minute      # Página principal
RATE_LIMIT_WEB_CONVERT=10 per minute    # Conversión desde formulario

# API REST
RATE_LIMIT_API_CONVERT=10 per minute    # Conversión desde API
RATE_LIMIT_API_HEALTH=60 per minute     # Health check
```

**Formatos válidos:**
- `"10 per minute"` - 10 peticiones por minuto
- `"100 per hour"` - 100 peticiones por hora
- `"1000 per day"` - 1000 peticiones por día
- `"unlimited"` o `"0"` - Sin límite (ilimitado)

**Ejemplos de uso:**
```env
# Para uso personal (sin límites)
RATE_LIMIT_API_CONVERT=unlimited

# Para servidor público (límites estrictos)
RATE_LIMIT_API_CONVERT=5 per minute

# Para uso interno empresarial (límites altos)
RATE_LIMIT_API_CONVERT=1000 per hour
```

## Requisitos

- Docker
- Docker Compose (opcional, pero recomendado)

## Instalación y Uso

### Opción 1: Usando Docker Compose (Recomendado)

1. Clona este repositorio:
```bash
git clone https://github.com/javiervilchezl/MdToPdf.git
cd MdToPdf
```

2. Construye y ejecuta el contenedor:
```bash
docker-compose up --build
```

3. Abre tu navegador en: `http://localhost:5000`

### Opción 2: Usando Docker directamente

1. Construye la imagen:
```bash
docker build -t md-to-pdf .
```

2. Ejecuta el contenedor:
```bash
docker run -p 5000:5000 md-to-pdf
```

3. Abre tu navegador en: `http://localhost:5000`

### Opción 3: Ejecución local (sin Docker)

1. Crea un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python app.py
```

4. Abre tu navegador en: `http://localhost:5000`

## Cómo usar

1. Abre la aplicación en tu navegador
2. Escribe o pega tu contenido Markdown en el área de texto
3. Haz clic en "Generar PDF"
4. El PDF se descargará automáticamente

## Uso de la API REST

### Endpoints Disponibles

#### `POST /api/convert`
Convierte Markdown a PDF. Acepta JSON y retorna un archivo PDF.

**⚠️ Requiere API Key OBLIGATORIAMENTE**

**Request (con autenticación):**
```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu-api-key-super-secreta-aqui" \
  -d '{"markdown": "# Hola Mundo\n\nEsto es **negrita**"}' \
  --output documento.pdf
```

**Request Body:**
```json
{
  "markdown": "# Tu contenido Markdown aquí..."
}
```

**Response:** 
- Success (200): Archivo PDF binario
- Error (400): `{"error": "mensaje de error"}`
- Error (401): `{"error": "API Key requerida", "message": "Incluye el header X-API-Key en tu petición"}`
- Error (403): `{"error": "API Key inválida", "message": "La API Key proporcionada no es válida"}`
- Error (500): `{"error": "mensaje de error"}`

#### `GET /api/health`
Endpoint de healthcheck para monitoreo.

**Response:**
```json
{
  "status": "healthy",
  "service": "markdown-to-pdf",
  "version": "1.0.0"
}
```

### Ejemplos de Uso

**Con cURL:**
```bash
# Convertir Markdown desde línea de comando
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d @- --output resultado.pdf << 'EOF'
{
  "markdown": "# Mi Documento\n\n## Sección 1\n\nContenido con **negrita** y *cursiva*.\n\n- Item 1\n- Item 2"
}
EOF
```

**Con Python:**
```python
import requests

markdown_content = """
# Mi Documento

## Introducción
Este es un documento de prueba.

| Columna 1 | Columna 2 |
|-----------|-----------|
| Dato A    | Dato B    |
"""

# Headers con API Key (OBLIGATORIA)
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'tu-api-key-super-secreta-aqui'  # REQUERIDA
}

response = requests.post(
    'http://localhost:5000/api/convert',
    json={'markdown': markdown_content},
    headers=headers
)

if response.status_code == 200:
    with open('resultado.pdf', 'wb') as f:
        f.write(response.content)
    print("PDF generado exitosamente")
else:
    print(f"Error {response.status_code}: {response.json()}")
```

**Con JavaScript/Node.js:**
```javascript
const fs = require('fs');
const fetch = require('node-fetch');

const markdown = `
# Mi Documento
## Contenido
Texto con **formato**.
`;

// Headers con API Key (OBLIGATORIA)
const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': 'tu-api-key-super-secreta-aqui'  // REQUERIDA
};

fetch('http://localhost:5000/api/convert', {
  method: 'POST',
  headers: headers,
  body: JSON.stringify({ markdown })
})
.then(async res => {
  if (res.ok) {
    const buffer = await res.buffer();
    fs.writeFileSync('documento.pdf', buffer);
    console.log('PDF generado');
  } else {
    const error = await res.json();
    console.error(`Error ${res.status}:`, error);
  }
})
.catch(err => console.error('Error:', err));
```

## Ejemplo de Markdown

```markdown
# Mi Documento

## Introducción

Este es un ejemplo de **Markdown**. Puedes usar:

- Listas
- *Cursiva* y **negrita**
- [Enlaces](https://ejemplo.com)

### Código

```python
def hola():
    print('¡Hola Mundo!')
```

### Tabla

| Columna 1 | Columna 2 |
|-----------|-----------|
| Dato 1    | Dato 2    |
| Dato 3    | Dato 4    |
```

## Estructura del Proyecto

```
md-to-pdf/
│
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Orquestación de Docker
├── README.md             # Este archivo
│
└── templates/
    └── index.html        # Interfaz web
```

## Tecnologías Utilizadas

- **Flask**: Framework web de Python
- **markdown2**: Conversión de Markdown a HTML
- **WeasyPrint**: Generación de PDF desde HTML
- **Docker**: Contenedorización
- **HTML/CSS/JavaScript**: Interfaz web

## Solución de Problemas

### El contenedor no inicia
- Verifica que Docker esté ejecutándose
- Asegúrate de que el puerto 5000 no esté en uso
- Revisa los logs: `docker-compose logs`

### Error al generar PDF
- Verifica que el contenido Markdown sea válido
- Revisa los logs del contenedor para más detalles

### Problemas con caracteres especiales
- Asegúrate de usar codificación UTF-8
- La aplicación soporta caracteres especiales y emojis

## Configuración de Seguridad

La aplicación incluye múltiples capas de seguridad:
- ✅ **Autenticación con API Key OBLIGATORIA** para todos los endpoints (excepto healthcheck)
- ✅ **Rate Limiting Configurable** - Ajusta límites o desactívalo con `unlimited` en `.env`
- ✅ Límite de tamaño de archivo (16MB)
- ✅ Validación estricta de entrada
- ✅ Timeout de operaciones
- ✅ Headers de seguridad HTTP
- ✅ Protección contra fuerza bruta

**IMPORTANTE para producción:**
- ⚠️ Configura SIEMPRE una API Key fuerte: `openssl rand -hex 32`
- ⚠️ Usa HTTPS (configura un proxy reverso con nginx)
- ⚠️ Cambia `FLASK_DEBUG=False`
- ⚠️ Ajusta los límites de rate limiting según tus necesidades:
  - Uso personal: `unlimited`
  - Servidor público: `5-10 per minute`
  - Uso empresarial: `1000 per hour`
- ⚠️ Monitorea los logs para detectar intentos de acceso no autorizado

## Producción

Para deploying en producción, considera:

1. **Configurar API Key:**
   ```bash
   export API_KEY="tu-api-key-super-secreta-y-larga-aqui-$(openssl rand -hex 32)"
   ```

2. **Desactivar debug mode:**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. Usar un servidor WSGI como Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

4. **Configurar un proxy reverso (nginx) con HTTPS:**
   ```nginx
   server {
       listen 443 ssl;
       server_name tu-dominio.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header X-API-Key $http_x_api_key;
       }
   }
   ```

5. **Limitar rate limiting** con nginx o un load balancer
6. **Monitorear** usando el endpoint `/api/health`

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Creado para convertir fácilmente Markdown a PDF sin necesidad de subir documentos con datos sensibles a ninguna web de terceros.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio.

---

¡Disfruta convirtiendo Markdown a PDF!
