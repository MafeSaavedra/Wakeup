import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep, splev
from math import degrees, acos

# Coordenadas de M1 a M11 (de arriba hacia abajo)
nombres = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11']
x = [-3.23, -4.47, -11.06, -13.96, -14.81, -13.30, -10.85, -10.95, -15.96, -16.72, -15.88]
y = [58.13, 52.56, 47.52, 39.40, 27.76, 17.95, 9.30, 1.14, -7.88, -13.00, -19.77]

# Punto M0 como referencia de origen
x0, y0 = -0.20, 0.22
x = [xi - x0 for xi in x]
y = [yi - y0 for yi in y]

# Crear spline suavizado
tck, u = splprep([x, y], s=0.5)
unew = np.linspace(0, 1.0, 500)
x_spline, y_spline = splev(unew, tck)

# Calcular el ángulo en M7 entre los vectores M6-M7 y M8-M7
p6 = np.array([x[5], y[5]])
p7 = np.array([x[6], y[6]])
p8 = np.array([x[7], y[7]])

v1 = p6 - p7
v2 = p8 - p7

# Calcular el ángulo entre los vectores
cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
angle_rad = acos(np.clip(cos_angle, -1.0, 1.0))
angle_mayor = round(degrees(angle_rad), 2)      # Ángulo externo
angle_menor = round(180 - angle_mayor, 2)        # Ángulo interno (lordosis real)

# Escalar vectores para graficar líneas
scale = 2.5
line1_start = p7 - scale * v1
line1_end   = p7 + scale * v1

line2_start = p7 - scale * v2
line2_end   = p7 + scale * v2

# Graficar
plt.figure(figsize=(6, 10))
plt.plot(x_spline, y_spline, color='blue', label='Spline Suavizado')
plt.plot(x, y, 'o', color='red')  # Puntos originales

# Etiquetar los puntos
for i, name in enumerate(nombres):
    plt.text(x[i], y[i], name, fontsize=9, ha='right')

# Dibujar líneas de los vectores
plt.plot([line1_start[0], line1_end[0]], [line1_start[1], line1_end[1]], 'g--', linewidth=1.8, label='M6–M7 extendida')
plt.plot([line2_start[0], line2_end[0]], [line2_start[1], line2_end[1]], 'm--', linewidth=1.8, label='M8–M7 extendida')

# Mostrar ángulos en M7
plt.text(p7[0] + 2, p7[1] + 2, f'Ángulo mayor: {angle_mayor}°', fontsize=9, color='darkgreen')
plt.text(p7[0] + 2, p7[1] - 2, f'Ángulo menor: {angle_menor}°', fontsize=9, color='darkred')

# Ejes y estilo
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')

plt.title('Ángulos en M7 (curvatura espinal)')
plt.xlabel('X (cm) - eje transversal')
plt.ylabel('Y (cm) - eje longitudinal')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.tight_layout()
plt.show()
