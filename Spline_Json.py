import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep, splev
from math import degrees, acos
import tkinter as tk
from tkinter import filedialog

# --- Selección del archivo ---
root = tk.Tk()
root.withdraw()
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo JSON del paciente",
    filetypes=[("Archivos JSON", "*.json")]
)

if not ruta_archivo:
    print("❌ No se seleccionó ningún archivo.")
    exit()

print(f"✅ Archivo seleccionado: {ruta_archivo}")

# --- Cargar y procesar JSON ---
with open(ruta_archivo, 'r', encoding='utf-8') as f:
    datos = json.load(f)

posiciones = datos["data"]["positions"]

# --- Extraer puntos ---
puntos = {}
for pos in posiciones:
    nombre = pos["name"]
    valor = pos["value"]
    if nombre == "M0":
        puntos["M0"] = valor
    elif nombre.startswith("Marcador "):
        try:
            idx = int(nombre.split()[-1])
            if 1 <= idx <= 11:
                puntos[f"M{idx}"] = valor
        except ValueError:
            continue

nombres = [f"M{i}" for i in range(1, 12)]

# --- Verificar si todos los marcadores están presentes ---
faltantes = [n for n in nombres if n not in puntos]
if faltantes:
    print(f"❌ Faltan los siguientes marcadores: {faltantes}")
    exit()

# --- Extraer coordenadas y centrar en M0 ---
x = [puntos[n][0] for n in nombres]
y = [puntos[n][1] for n in nombres]
x0, y0 = puntos["M0"]
x = [xi - x0 for xi in x]
y = [yi - y0 for yi in y]

# --- Reorientar curva para que apunte al eje Y (verticalizar) ---
v_ref = np.array([x[0], y[0]])  # Vector M1 respecto a M0
angulo_ref = np.arctan2(v_ref[1], v_ref[0])
angulo_rot = -angulo_ref + np.pi / 2

cos_a = np.cos(angulo_rot)
sin_a = np.sin(angulo_rot)
R = np.array([[cos_a, -sin_a],
              [sin_a,  cos_a]])

rotados = np.dot(R, np.vstack((x, y)))
x, y = rotados[0], rotados[1]

# --- Crear spline suavizado ---
tck, u = splprep([x, y], s=0.5)
unew = np.linspace(0, 1.0, 500)
x_spline, y_spline = splev(unew, tck)

# --- Calcular ángulo en M7 ---
p6 = np.array([x[5], y[5]])
p7 = np.array([x[6], y[6]])
p8 = np.array([x[7], y[7]])

v1 = p6 - p7
v2 = p8 - p7

cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
angle_rad = acos(np.clip(cos_angle, -1.0, 1.0))
angle_mayor = round(degrees(angle_rad), 2)
angle_menor = round(180 - angle_mayor, 2)

# --- Vectores extendidos para dibujo ---
scale = 2.5
line1_start = p7 - scale * v1
line1_end   = p7 + scale * v1
line2_start = p7 - scale * v2
line2_end   = p7 + scale * v2

# --- Cálculo de ángulo con respecto al eje Y ---
inicio = np.array([x[0], y[0]])
final  = np.array([x[-1], y[-1]])
vector_total = final - inicio
norma = np.linalg.norm(vector_total)
vector_eje_y = np.array([0, 1])
cos_eje_y = np.dot(vector_total, vector_eje_y) / norma
angulo_vertical = degrees(acos(np.clip(cos_eje_y, -1.0, 1.0)))

print(f"Ángulo entre la curva M1–M11 y el eje Y: {round(angulo_vertical, 2)}°")

# --- Graficar ---
plt.figure(figsize=(6, 10))
plt.plot(x_spline, y_spline, color='blue', label='Spline Suavizado')
plt.plot(x, y, 'o', color='red')  # Puntos originales

for i, name in enumerate(nombres):
    plt.text(x[i], y[i], name, fontsize=9, ha='right')

plt.plot([line1_start[0], line1_end[0]], [line1_start[1], line1_end[1]], 'g--', linewidth=1.8, label='M6–M7 extendida')
plt.plot([line2_start[0], line2_end[0]], [line2_start[1], line2_end[1]], 'm--', linewidth=1.8, label='M8–M7 extendida')

plt.text(p7[0] + 2, p7[1] + 2, f'Ángulo mayor: {angle_mayor}°', fontsize=9, color='darkgreen')
plt.text(p7[0] + 2, p7[1] - 2, f'Ángulo menor: {angle_menor}°', fontsize=9, color='darkred')

plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')

plt.title('Ángulos en M7 y Verificación de Verticalización')
plt.xlabel('X (cm) - eje transversal')
plt.ylabel('Y (cm) - eje longitudinal')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.tight_layout()
plt.show()
