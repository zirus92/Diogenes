import socket
import os
import sys

def mostrar_menu1():
    os.system("clear")
    os.system("figlet -f slant 'DIOGENES' | lolcat")
    os.system('echo "\e[31m[\e[0m1\e[31m]\e[0m Una sola consulta"')
    os.system('echo "\e[31m[\e[0m2\e[31m]\e[0m Consulta por lote"')
    os.system('echo "\e[31m[\e[0m0\e[31m]\e[0m Salir"')

def mostrar_menu2():
    os.system("clear")
    os.system("figlet -f slant 'Diogenes' | lolcat")
    os.system('echo "\e[31m[\e[0m1\e[31m]\e[0m IP a Dominio"')
    os.system('echo "\e[31m[\e[0m2\e[31m]\e[0m Dominio a IP"')
    os.system('echo "\e[31m[\e[0m0\e[31m]\e[0m Salir"')

def convertir_ip_a_dominio(ip):
    try:
        dominio = socket.gethostbyaddr(ip)[0]
        return f'{ip} -> {dominio}'
    except socket.herror:
        return f'{ip} -> No se pudo resolver'
    except OSError:
        return f'{ip} -> Resuelve a múltiples direcciones'

def convertir_dominio_a_ip(dominio):
    try:
        ip = socket.gethostbyname(dominio)
        return f'{dominio} -> {ip}'
    except socket.gaierror:
        return f'{dominio} -> No se pudo resolver'

def consulta_individual(opcion):
    if opcion == '1':
        ip = input("Introduce la IP: ")
        print(convertir_ip_a_dominio(ip))
    elif opcion == '2':
        dominio = input("Introduce el dominio: ")
        print(convertir_dominio_a_ip(dominio))

def consulta_por_lote(opcion):
    archivo_entrada = input("Introduce el nombre del archivo de entrada: ")
    archivo_salida = archivo_entrada.split('.')[0] + '-salida.txt'
    
    with open(archivo_entrada, 'r') as archivo:
        lineas = archivo.read().splitlines()

    resultados = []
    if opcion == '1':
        for ip in lineas:
            resultados.append(convertir_ip_a_dominio(ip))
    elif opcion == '2':
        for dominio in lineas:
            resultados.append(convertir_dominio_a_ip(dominio))
    
    with open(archivo_salida, 'w') as archivo:
        for resultado in resultados:
            archivo.write(resultado + '\n')
    
    print(f"Los resultados se han guardado en '{archivo_salida}'")

def main():
    mostrar_menu1()
    opcion_menu1 = input("Selecciona una opción: ")
    if opcion_menu1 == '0':
        print("Saliendo...")
        sys.exit()

    mostrar_menu2()
    opcion_menu2 = input("Selecciona una opción: ")
    if opcion_menu2 == '0':
        print("Saliendo...")
        sys.exit()

    if opcion_menu1 == '1':
        consulta_individual(opcion_menu2)
    elif opcion_menu1 == '2':
        consulta_por_lote(opcion_menu2)
    else:
        print("Opción no válida")

if __name__ == "__main__":
    main()
