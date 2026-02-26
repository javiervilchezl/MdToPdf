from flask import Flask, render_template, request, send_file, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from dotenv import load_dotenv
import markdown2
from weasyprint import HTML, CSS
from io import BytesIO
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
API_KEY = os.getenv('API_KEY')  # API Key OBLIGATORIA desde .env

# Verificar que existe API_KEY
if not API_KEY:
    raise ValueError(
        "⚠️  API_KEY no configurada! "
        "Crea un archivo .env con tu API_KEY "
        "(usa .env.example como plantilla)"
    )

# Configurar Rate Limiting (protección contra fuerza bruta)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[os.getenv('RATE_LIMIT_DEFAULT', '20 per minute')],
    storage_uri=os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')
)


def require_api_key(f):
    """
    Decorador para requerir API Key en todos los endpoints.
    La API Key puede venir de:
    - Header 'X-API-Key' (para API REST)
    - Form field 'api_key' (para interfaz web)
    - Query parameter 'api_key' (alternativa)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener API Key de diferentes fuentes
        provided_key = (
            request.headers.get('X-API-Key') or
            request.form.get('api_key') or
            request.args.get('api_key')
        )
        
        if not provided_key:
            # Si es una petición JSON, responder con JSON
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'error': 'API Key requerida',
                    'message': 'Incluye el header X-API-Key en tu petición'
                }), 401
            # Si es interfaz web, mostrar mensaje HTML
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Key Requerida</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                        max-width: 500px;
                    }
                    h1 { color: #333; margin-bottom: 20px; }
                    p { color: #666; line-height: 1.6; }
                    code {
                        background: #f4f4f4;
                        padding: 2px 6px;
                        border-radius: 3px;
                        color: #e83e8c;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔐 API Key Requerida</h1>
                    <p>Este microservicio requiere autenticación.</p>
                    <p>Accede con tu API Key mediante:</p>
                    <ul style="text-align: left; color: #666;">
                        <li>URL: <code>?api_key=TU_CLAVE</code></li>
                        <li>Header: <code>X-API-Key: TU_CLAVE</code></li>
                    </ul>
                    <p style="margin-top: 20px; color: #999; font-size: 14px;">
                        Contacta al administrador para obtener tu API Key
                    </p>
                </div>
            </body>
            </html>
            ''', 401
        
        if provided_key != API_KEY:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({
                    'error': 'API Key inválida',
                    'message': 'La API Key proporcionada no es válida'
                }), 403
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Key Inválida</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                    }
                    h1 { color: #e74c3c; }
                    p { color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>❌ API Key Inválida</h1>
                    <p>La API Key proporcionada no es válida.</p>
                    <p>Verifica tu configuración e intenta nuevamente.</p>
                </div>
            </body>
            </html>
            ''', 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def process_markdown_to_pdf(markdown_content):
    """
    Función helper para convertir Markdown a PDF.
    Retorna un BytesIO con el PDF generado.
    """
    if not markdown_content:
        raise ValueError("No se proporcionó contenido Markdown")
    
    # Preprocesar: Asegurar línea en blanco antes de tablas
    lines = markdown_content.split('\n')
    processed_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and i > 0:
            prev_line = lines[i-1].strip()
            if prev_line and not prev_line.startswith('|'):
                if processed_lines and processed_lines[-1].strip():
                    processed_lines.append('')
        processed_lines.append(line)
    
    markdown_content = '\n'.join(processed_lines)
    
    # Convertir Markdown a HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=[
            'tables',
            'fenced-code-blocks',
            'strike',
            'task_list'
        ]
    )
    
    # CSS para mejorar el estilo del PDF
    css_style = """
    @page {
        margin: 1.2cm 0.8cm;
        size: A4 portrait;
    }
    body {
        font-family: 'Arial', 'Helvetica', sans-serif;
        line-height: 1.4;
        color: #222;
        font-size: 9pt;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        margin-top: 0.6em;
        margin-bottom: 0.3em;
    }
    h1 {
        font-size: 16pt;
        border-bottom: 2px solid #2c3e50;
        padding-bottom: 0.2em;
    }
    h2 {
        font-size: 13pt;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 0.2em;
    }
    h3 {
        font-size: 11pt;
    }
    code {
        background-color: #f4f4f4;
        padding: 2px 4px;
        border-radius: 2px;
        font-family: 'Courier New', monospace;
        font-size: 8pt;
    }
    pre {
        background-color: #f4f4f4;
        padding: 8px;
        border-radius: 3px;
        border-left: 3px solid #3498db;
        overflow: visible;
        white-space: pre-wrap;
        word-wrap: break-word;
        page-break-inside: avoid;
        margin: 0.5em 0;
    }
    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 7pt;
        white-space: pre-wrap;
        word-break: break-word;
    }
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 15px;
        color: #555;
        font-style: italic;
        margin: 1em 0;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 0.5em 0;
        page-break-inside: auto;
        font-size: 6.5pt;
        table-layout: fixed;
    }
    table th, table td {
        border: 1px solid #555;
        padding: 3px 4px;
        text-align: left;
        word-wrap: break-word;
        vertical-align: top;
        overflow-wrap: anywhere;
        line-height: 1.25;
        hyphens: auto;
    }
    table th {
        background-color: #2c7cbd;
        color: white;
        font-weight: bold;
        font-size: 6.5pt;
    }
    table tr:nth-child(even) {
        background-color: #f8f8f8;
    }
    table tr {
        page-break-inside: avoid;
    }
    table code {
        font-size: 6pt;
        word-break: break-word;
        white-space: normal;
    }
    a {
        color: #3498db;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    ul, ol {
        margin: 1em 0;
        padding-left: 2em;
    }
    li {
        margin: 0.5em 0;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    """
    
    # Crear el HTML completo
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Documento PDF</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generar PDF
    pdf_buffer = BytesIO()
    html_obj = HTML(string=full_html)
    pdf_bytes = html_obj.write_pdf(stylesheets=[CSS(string=css_style)])
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
    
    return pdf_buffer


@app.route('/')
@limiter.limit("20 per minute")
@require_api_key
def index():
    """Página principal con el formulario"""
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def convert_to_pdf():
    """Endpoint web: Convierte el contenido Markdown a PDF desde formulario"""
    try:
        markdown_content = request.form.get('markdown_content', '')
        pdf_buffer = process_markdown_to_pdf(markdown_content)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='documento.pdf'
        )
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500


@app.route('/api/convert', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def api_convert_to_pdf():
    """
    Endpoint API REST: Convierte Markdown a PDF desde JSON.
    Requiere API Key obligatoriamente.
    """
    try:
        # Validar Content-Type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        markdown_content = data.get('markdown', '')
        
        if not markdown_content:
            return jsonify({
                'error': 'El campo "markdown" es requerido'
            }), 400
        
        pdf_buffer = process_markdown_to_pdf(markdown_content)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='documento.pdf'
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al generar PDF: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
@limiter.limit("60 per minute")
def api_health():
    """Endpoint de healthcheck para monitoreo (sin autenticación)"""
    return jsonify({
        'status': 'healthy',
        'service': 'markdown-to-pdf',
        'version': '1.0.0'
    }), 200


if __name__ == '__main__':
    # Usar variable de entorno para debug
    debug_env = os.getenv('FLASK_DEBUG', 'False').lower()
    debug_mode = debug_env in ('true', '1', 't')
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
