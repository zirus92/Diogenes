import os
import subprocess

# Función para mostrar el menú
def mostrar_menu():
    os.system('clear')
    subprocess.run("figlet -f slant 'DIOGENES' | lolcat", shell=True)
    os.system('echo "\e[31m[\e[0m1\e[31m]\e[0m Buscar subdominios y asociados"')
    os.system('echo "\e[31m[\e[0m2\e[31m]\e[0m Escanear de subdominios"')
    os.system('echo "\e[31m[\e[0m3\e[31m]\e[0m Convertir IP a dominio"')
    os.system('echo "\e[31m[\e[0m0\e[31m]\e[0m Salir"')
    print("\nSelecciona una opción: ", end='')

def esperar_para_continuar():
    input("Presiona Enter para volver al menú...")

# Lógica principal
def main():
    while True:
        mostrar_menu()
        opcion = input()
        
        if opcion == '1':
            subprocess.run("python3 buscador_dominios.py", shell=True)
            esperar_para_continuar()
        elif opcion == '2':
            subprocess.run("python3 comprobador.py", shell=True)
            esperar_para_continuar()
        elif opcion == '3':
            subprocess.run("python3 convertir_ips.py", shell=True)
            esperar_para_continuar()
        elif opcion == '0':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
