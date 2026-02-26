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

**Request:**
```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
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

response = requests.post(
    'http://localhost:5000/api/convert',
    json={'markdown': markdown_content}
)

if response.status_code == 200:
    with open('resultado.pdf', 'wb') as f:
        f.write(response.content)
    print("PDF generado exitosamente")
else:
    print(f"Error: {response.json()}")
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

fetch('http://localhost:5000/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ markdown })
})
.then(res => res.buffer())
.then(buffer => {
  fs.writeFileSync('documento.pdf', buffer);
  console.log('PDF generado');
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

La aplicación incluye:
- Límite de tamaño de archivo (16MB)
- Validación de entrada
- Timeout de operaciones

## Producción

Para deploying en producción, considera:

1. Cambiar `debug=True` a `debug=False` en `app.py`
2. Usar un servidor WSGI como Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Configurar variables de entorno apropiadas
4. Implementar autenticación si es necesario
5. Configurar un proxy reverso (nginx)

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
