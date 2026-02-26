from flask import Flask, render_template, request, send_file
import markdown2
from weasyprint import HTML, CSS
from io import BytesIO
import os

app = Flask(__name__)

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    """Convierte el contenido Markdown a PDF"""
    try:
        # Obtener el contenido del textarea
        markdown_content = request.form.get('markdown_content', '')
        
        if not markdown_content:
            return "No se proporcionó contenido Markdown", 400
        
        # Preprocesar: Asegurar línea en blanco antes de tablas
        # Las tablas en Markdown necesitan una línea vacía antes para ser reconocidas
        import re
        lines = markdown_content.split('\n')
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Si la línea actual es el inicio de una tabla (contiene |)
            # y la línea anterior no está vacía, agregamos una línea vacía
            if line.strip().startswith('|') and i > 0:
                prev_line = lines[i-1].strip()
                # Si la línea anterior no está vacía y no es parte de la tabla
                if prev_line and not prev_line.startswith('|'):
                    # Si la última línea procesada no está vacía, agregar línea vacía
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
        
        # Debug: Ver si hay tablas en el HTML generado
        table_count = html_content.count('<table>')
        if table_count > 0:
            print(f"[DEBUG] Se encontraron {table_count} tablas en el HTML")
        else:
            print(f"[DEBUG] NO se encontraron tablas. Primeros 1000 chars del markdown: {markdown_content[:1000]}")
            print(f"[DEBUG] Primeros 1000 chars del HTML: {html_content[:1000]}")
        
        
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
        
        # Enviar el archivo PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='documento.pdf'
        )
        
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500

if __name__ == '__main__':
    # Usar variable de entorno para debug, por defecto False para producción
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
