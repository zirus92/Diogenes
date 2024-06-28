import subprocess
import os
import requests
from bs4 import BeautifulSoup
import dns.resolver
import argparse
from urllib.parse import urlparse
from tqdm import tqdm

# Función para imprimir el banner
def print_banner():
    os.system('clear')
    subprocess.run("figlet -f slant 'DIOGENES' | lolcat", shell=True)

# Función para buscar subdominios
def find_subdomains(domain):
    subdomains = set()
    
    # Usar diversas fuentes para buscar subdominios
    # Fuente 1: API de CRT.SH
    try:
        response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json")
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                subdomains.update(entry['name_value'].split())
    except Exception as e:
        print(f"Error fetching from crt.sh: {e}")

    # Fuente 2: Scraping motores de búsqueda (Google)
    try:
        google_search = requests.get(f"https://www.google.com/search?q=site:{domain}")
        soup = BeautifulSoup(google_search.text, 'html.parser')
        for link in soup.find_all('a'):
            url = link.get('href')
            if domain in url:
                parsed_url = urlparse(url)
                if parsed_url.netloc.endswith(domain):
                    subdomains.add(parsed_url.netloc)
    except Exception as e:
        print(f"Error scraping Google: {e}")

    # Fuente 3: Scraping motores de búsqueda (Yahoo)
    try:
        yahoo_search = requests.get(f"https://search.yahoo.com/search?p=site:{domain}")
        soup = BeautifulSoup(yahoo_search.text, 'html.parser')
        for link in soup.find_all('a'):
            url = link.get('href')
            if domain in url:
                parsed_url = urlparse(url)
                if parsed_url.netloc.endswith(domain):
                    subdomains.add(parsed_url.netloc)
    except Exception as e:
        print(f"Error scraping Yahoo: {e}")

    # Fuente 4: Scraping motores de búsqueda (Yandex)
    try:
        yandex_search = requests.get(f"https://yandex.com/search/?text=site:{domain}")
        soup = BeautifulSoup(yandex_search.text, 'html.parser')
        for link in soup.find_all('a'):
            url = link.get('href')
            if domain in url:
                parsed_url = urlparse(url)
                if parsed_url.netloc.endswith(domain):
                    subdomains.add(parsed_url.netloc)
    except Exception as e:
        print(f"Error scraping Yandex: {e}")

    # Filtrar subdominios vacíos y con comodines
    subdomains = {subdomain for subdomain in subdomains if subdomain and '*' not in subdomain}

    return subdomains

# Función para buscar dominios relacionados
def find_related_domains(domain, subdomains):
    related_domains = set()
    # Usar consultas DNS con un tiempo de espera extendido
    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10

    for subdomain in tqdm(subdomains, desc="Buscando dominios relacionados"):
        try:
            answers = resolver.resolve(subdomain, 'A')
            for rdata in answers:
                ip = str(rdata)
                try:
                    # Resolver IP a dominio
                    reverse_name = dns.reversename.from_address(ip)
                    reverse_domains = resolver.resolve(reverse_name, 'PTR')
                    for ptr in reverse_domains:
                        related_domains.add(str(ptr).strip('.'))
                except:
                    pass
        except dns.resolver.NXDOMAIN:
            print(f"Error resolving DNS for {subdomain}: The DNS query name does not exist.")
        except dns.resolver.Timeout:
            print(f"Error resolving DNS for {subdomain}: The DNS operation timed out.")
        except dns.resolver.NoAnswer:
            print(f"Error resolving DNS for {subdomain}: The DNS response does not contain an answer.")
        except Exception as e:
            print(f"Error resolving DNS for {subdomain}: {e}")

    # Relaciones adicionales
    try:
        response = requests.get(f"https://www.threatminer.org/domain.php?q={domain}&rt=5")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                url = link.get('href')
                if domain in url:
                    parsed_url = urlparse(url)
                    if parsed_url.netloc:
                        related_domains.add(parsed_url.netloc)
    except Exception as e:
        print(f"Error fetching related domains from ThreatMiner: {e}")

    return related_domains

def main():
    print_banner()

    # Solicitar el dominio al usuario
    domain = input("Ingrese el nombre del dominio principal (o '0' para salir): ")
    
    # Si el usuario ingresa '0', detener el script
    if domain == '0':
        print("Saliendo del script...")
        return

    # Buscar subdominios
    print("Buscando subdominios...")
    subdomains = find_subdomains(domain)
    subdomains_filename = domain.replace('.', '') + '_subdominios.txt'
    with open(subdomains_filename, 'w') as f:
        for subdomain in subdomains:
            f.write(subdomain + '\n')

    # Buscar dominios relacionados
    print("Buscando dominios relacionados...")
    related_domains = find_related_domains(domain, subdomains)
    related_domains_filename = domain.replace('.', '') + '_relaciones.txt'
    with open(related_domains_filename, 'w') as f:
        for related_domain in related_domains:
            clean_domain = related_domain.split('/')[0]
            f.write(clean_domain + '\n')

    print(f"Búsqueda completada. Resultados guardados en {subdomains_filename} y {related_domains_filename}")

if __name__ == "__main__":
    main()
