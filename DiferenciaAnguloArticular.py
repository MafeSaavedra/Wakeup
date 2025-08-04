import json
import math
import tkinter as tk
from tkinter import filedialog

def calcular_angulo_vertical(p_origen, p_objetivo):
    dx = p_objetivo[0] - p_origen[0]
    dy = p_objetivo[1] - p_origen[1]
    magnitud = math.sqrt(dx**2 + dy**2)
    cos_theta = dy / magnitud
    angulo = math.degrees(math.acos(cos_theta))
    return angulo

def procesar_json(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    posiciones = data['data']['positions']
    
    M0 = MD = MI = None

    for marcador in posiciones:
        nombre = marcador['name'].strip().upper()
        if nombre == 'M0':
            M0 = marcador['value']
        elif nombre == 'MD':
            MD = marcador['value']
        elif nombre == 'MI':
            MI = marcador['value']

    if not (M0 and MD and MI):
        print("❌ Faltan uno o más marcadores (M0, MD, MI) en el archivo.")
        return

    angulo_MD = calcular_angulo_vertical(M0, MD)
    angulo_MI = calcular_angulo_vertical(M0, MI)
    diferencia = abs(angulo_MD - angulo_MI)

    print("✅ Resultados del análisis:")
    print(f"Ángulo M0 → MD (derecha): {angulo_MD:.2f}°")
    print(f"Ángulo M0 → MI (izquierda): {angulo_MI:.2f}°")
    print(f"Diferencia entre ángulos: {diferencia:.2f}°")

# === Selección del archivo JSON ===
root = tk.Tk()
root.withdraw()
ruta = filedialog.askopenfilename(
    title="Selecciona un archivo JSON de Kinovea",
    filetypes=[("Archivos JSON", "*.json")]
)

if ruta:
    procesar_json(ruta)
else:
    print("⚠️ No se seleccionó ningún archivo.")
