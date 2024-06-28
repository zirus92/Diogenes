import requests
import socket
import ssl
import sqlite3
from OpenSSL import SSL
from urllib.parse import urlparse
import os
import sys
from tqdm import tqdm

# Limpiar la consola y mostrar el mensaje
os.system('clear')
os.system("figlet -f slant 'DIOGENES' | lolcat")

# Solicitar el nombre del archivo
subdomain_file = input('Introduce el nombre del archivo de subdominios (e.g., subdomains.txt) o 0 para salir: ')

# Verificar si el usuario desea salir
if subdomain_file == '0':
    print("Ejecución detenida por el usuario.")
    sys.exit()

# Asignar nombre a la base de datos
db_file = subdomain_file.replace('.txt', '.db')

# Crear o conectar a la base de datos
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Crear tabla en la base de datos
cursor.execute('''
CREATE TABLE IF NOT EXISTS subdomains (
    subdomain TEXT,
    server TEXT,
    status_code INTEGER,
    tls_version TEXT,
    ip_address TEXT,
    has_cert INTEGER,
    cdn TEXT
)
''')

# Leer subdominios desde el archivo
with open(subdomain_file, 'r') as file:
    subdomains = file.read().splitlines()

# Función para obtener información del subdominio
def get_subdomain_info(subdomain):
    result = {
        'subdomain': subdomain,
        'server': 'Unknown',
        'status_code': 0,
        'tls_version': 'Unknown',
        'ip_address': 'Unknown',
        'has_cert': 0,
        'cdn': 'Unknown'
    }
    
    try:
        # Obtener código de estado y servidor
        response = requests.get(f'http://{subdomain}', timeout=10)
        result['status_code'] = response.status_code
        if 'Server' in response.headers:
            result['server'] = response.headers['Server']
        
        # Obtener dirección IP
        result['ip_address'] = socket.gethostbyname(subdomain)
        
        # Comprobar CDN
        if 'cloudflare' in response.headers.get('Server', '').lower():
            result['cdn'] = 'Cloudflare'
        elif 'cloudfront' in response.headers.get('Server', '').lower():
            result['cdn'] = 'Cloudfront'
        
        # Obtener versión de TLS y certificado SSL
        parsed_url = urlparse(f'https://{subdomain}')
        context = ssl.create_default_context()
        with socket.create_connection((parsed_url.netloc, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=parsed_url.netloc) as ssock:
                result['tls_version'] = ssock.version()
                cert = ssock.getpeercert()
                if cert:
                    result['has_cert'] = 1
        
    except Exception as e:
        print(f'Error obteniendo información de {subdomain}: {e}')
    
    return result

# Procesar cada subdominio con barra de carga
for subdomain in tqdm(subdomains, desc="Procesando subdominios"):
    info = get_subdomain_info(subdomain)
    cursor.execute('''
    INSERT INTO subdomains (subdomain, server, status_code, tls_version, ip_address, has_cert, cdn)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (info['subdomain'], info['server'], info['status_code'], info['tls_version'], info['ip_address'], info['has_cert'], info['cdn']))

# Guardar cambios y cerrar la base de datos
conn.commit()
conn.close()
