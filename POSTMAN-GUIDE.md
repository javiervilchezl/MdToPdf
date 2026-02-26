# 🧪 Instrucciones para probar en Postman

## URL del servicio
http://localhost:5000

---

## 📋 Endpoint API: POST /api/convert

### Configuración en Postman:

**1. Método:** `POST`

**2. URL:** `http://localhost:5000/api/convert`

**3. Headers:**
```
Content-Type: application/json
X-API-Key: mi-clave-secreta-de-prueba-123
```

**4. Body (selecciona "raw" y "JSON"):**
```json
{
  "markdown": "# Mi Documento\n\n## Introducción\nEste es un **test** desde Postman.\n\n### Lista:\n- Item 1\n- Item 2\n\n### Tabla\n\n| Col1 | Col2 |\n|------|------|\n| A    | B    |"
}
```

**5. Enviar:**
- Haz clic en **"Send and Download"** (no solo "Send")
- O después de enviar, haz clic en **"Save Response" → "Save to a file"**
- Guarda como `documento.pdf`

---

## 🔍 Respuestas esperadas:

### ✅ Con API Key correcta:
- **Status:** `200 OK`
- **Content-Type:** `application/pdf`
- **Body:** Archivo PDF binario (descargable)

### ❌ Sin API Key:
- **Status:** `401 Unauthorized`
- **Body:**
```json
{
  "error": "API Key requerida",
  "message": "Incluye el header X-API-Key en tu petición"
}
```

### ❌ Con API Key incorrecta:
- **Status:** `403 Forbidden`
- **Body:**
```json
{
  "error": "API Key inválida",
  "message": "La API Key proporcionada no es válida"
}
```

---

## 🌐 Interfaz Web (NO requiere API Key):

Abre en tu navegador:
- **Interfaz:** http://localhost:5000
- **Formulario:** http://localhost:5000/convert (POST desde el formulario)

Estos endpoints son **públicos** para uso humano directo.

---

## 🔐 Notas de seguridad:

1. La API Key se configura en el servidor (docker-compose.yml o .env)
2. Por defecto en desarrollo, si no hay API_KEY configurada, el endpoint queda abierto
3. En producción, SIEMPRE configura una API Key fuerte
4. La interfaz web permanece pública para uso del navegador
5. Solo el endpoint API REST `/api/convert` requiere autenticación

---

## 📝 Ejemplo con cURL (alternativa a Postman):

```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: mi-clave-secreta-de-prueba-123" \
  -d '{"markdown":"# Hola desde cURL"}' \
  --output resultado.pdf
```

---

## 💡 Tips:

1. En Postman puedes guardar esta petición en una Collection
2. Crea una variable de entorno para la API Key
3. Usa "Tests" en Postman para validar la respuesta automáticamente
4. Verifica que el Content-Type de la respuesta sea `application/pdf`
