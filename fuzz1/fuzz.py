import httpx, sys
from colorama import Fore, init
from fake_useragent import UserAgent
init()

try:
    dic=sys.argv[1]
    dominio=sys.argv[2]
except:
    print(Fore.RED+f"""
[!] Uso incorrecto.
Este script necesita 2 argumentos:
  1) Un archivo de diccionario con posibles subdominios (uno por línea).
  2) El dominio al que quieres hacerle el escaneo de subdominios.

Ejemplo de uso:
  python {sys.argv[0]} diccionario.txt ejemplo.com

Si no le pasas esos dos argumentos, no puedo saber qué probar ni sobre qué dominio.
""")
    sys.exit(1)
    
user_agent1 = UserAgent()
headersS = {
    "User-Agent": user_agent1.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1"
}
def Probar(url):
    try:
        r=httpx.get(url, follow_redirects=True, headers=headersS)
        return r.status_code
    except httpx.RequestError:
        return None
def Todo():
    try:
        with open(dic, "r") as dicc:
            subdominios=dicc.read().splitlines()
    except FileNotFoundError as vl:
        
        print(Fore.RED+f"Error: {vl}")
    print(Fore.GREEN+ "[?] Probando: ")
    for subdominio in subdominios:
        dom_completo= f"{subdominio}.{dominio}"

        https=f"https://{dom_completo}"
        status=Probar(https)
        print(f"\033[F[?] Probando: {https}    ")
        if status and status != 404:
            print(Fore.RED+f"[+]{https} -> {status}")

        http=f"http://{dom_completo}"
        status=Probar(http)
        print(f"\033[F[?] Probando: {http}    ")
        if status and status != 404:
            print(Fore.RED+f"[+]{http} -> {status}")
if __name__ == '__main__':
    Todo()
