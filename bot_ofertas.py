import requests
import time
import threading
from flask import Flask

# 🛍️ 1. TU URL DE DISCORD:
URL_MI_WEBHOOK = "https://discord.com/api/webhooks/1507247515869646901/H_vZBpFd1q6wpe1oeDWo_XQKOLjgzxM2_gpdNFv0hMior6EO_owMcL3s-BkCSjldMy_D" # Asegúrate de que esté tu webhook completo aquí

app = Flask(__name__)

@app.route('/')
def home():
    return "El bot de ofertazos está en línea y patrullando! 🚀"

def ciclo_bot():
    # Una pequeña pausa de 10 segundos al arrancar para darle tiempo a Render de ponerse cómodo
    time.sleep(10)
    
    url_mejores_ofertas = "https://www.cheapshark.com/api/1.0/deals?upperPrice=50&pageSize=30&sortBy=Metacritic"
    nombres_tiendas = {
        "1": "Steam", "25": "Epic Games Store", "7": "GOG", "3": "GreenManGaming", "11": "Humble Store"
    }
    
    while True:
        print("⏰ Iniciando el escaneo automático y filtrado de ofertas...")
        try:
            respuesta = requests.get(url_mejores_ofertas)
            if respuesta.status_code == 200:
                ofertas = respuesta.json()
                mensaje_discord = "🔥 🏷️ **¡EL TOP 5 DE OFERTAZOS DEL DÍA!** 🏷️ 🔥\n\n"
                
                juegos_agregados = set()
                contador_top = 1
                
                for juego in ofertas:
                    if contador_top > 5:
                        break
                        
                    titulo = juego['title']
                    precio_oferta = juego['salePrice']
                    precio_normal = juego['normalPrice']
                    ahorro = round(float(juego['savings']))
                    id_tienda = juego['storeID']
                    
                    if ahorro < 15:
                        continue
                        
                    if titulo in juegos_agregados:
                        continue
                    
                    juegos_agregados.add(titulo)
                    tienda = nombres_tiendas.get(id_tienda, "Otra tienda de PC")
                    
                    mensaje_discord += f"{contador_top}️⃣ **{titulo}**\n"
                    mensaje_discord += f"   🔹 Tienda: {tienda}\n"
                    mensaje_discord += f"   🔹 Descuento: ¡**{ahorro}% de DESCUENTO**!\n"
                    mensaje_discord += f"   🔹 Precio: ~~${precio_normal}~~ a **${precio_oferta} USD**\n\n"
                    
                    contador_top += 1
                
                if contador_top == 1:
                    mensaje_discord += "❌ Hoy no se encontraron ofertazos que superen los filtros de calidad."
                
                # Enviar reporte a Discord
                requests.post(URL_MI_WEBHOOK, json={"content": mensaje_discord})
                print("¡Ofertazos filtrados enviados a Discord con éxito! 🎉")
            else:
                print(f"Error en la API: {respuesta.status_code}")
        except Exception as e:
            print(f"Error inesperado en el bot: {e}")

        # Se duerme por 24 horas antes de la siguiente búsqueda
        print("😴 Escaneo finalizado. Durmiendo por 24 horas...")
        time.sleep(86400)

# El truco maestro: Primero declaramos el arranque principal de Python
if __name__ == "__main__":
    # 1. Encendemos el bot en su propio hilo secundario para que no estorbe
    threading.Thread(target=ciclo_bot, daemon=True).start()
    
    # 2. De inmediato encendemos Flask en el hilo principal para responderle a Render rápido
    print("Iniciando servidor web falso para Render...")
    app.run(host="0.0.0.0", port=10000)