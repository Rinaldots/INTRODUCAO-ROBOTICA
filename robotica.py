# Robótica: Cinemática Direta de Manipulador
# Este script realiza a calibração dos servos, cálculo dos ângulos das juntas e a cinemática direta de um braço robótico, além de visualizar o espaço de trabalho em 3D.

import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
import pandas as pd

# Matrizes de rotação e parâmetros do robô
o1 = 0
o2 = 0
o3 = 0
o4 = 0
L1 = 14.5/100
L2 = 18.2/100
L3 = 9.0/100
h = 7.5/100

# Calibração dos servos
servo_0_0 = 1530
servo_1_0 = 700
servo_2_0 = 640
servo_3_0 = 1505
servo_0_90 = 640
servo_1_90 = 1460
servo_2_270 = 1455
servo_3_270 = 725

angles = np.array([0, 90, 270])
servo_0_values = np.array([servo_0_0, servo_0_90])
servo_1_values = np.array([servo_1_0, servo_1_90])
servo_2_values = np.array([servo_2_0, servo_2_270])
servo_3_values = np.array([servo_3_0, servo_3_270])

a0 = (servo_0_values[1] - servo_0_values[0]) / (angles[1] - angles[0])
a1 = (servo_1_values[1] - servo_1_values[0]) / (angles[1] - angles[0])
a2 = (servo_2_values[1] - servo_2_values[0]) / (angles[2] - angles[0])
a3 = (servo_3_values[1] - servo_3_values[0]) / (angles[2] - angles[0])

b0 = servo_0_values[0] - a0 * angles[0]
b1 = servo_1_values[0] - a1 * angles[0]
b2 = servo_2_values[0] - a2 * angles[0]
b3 = servo_3_values[0] - a3 * angles[0]

def servo_angle(servo_value, a, b):
    return (servo_value - b) / a

# Função para converter ângulo (graus) para PWM
def angle_to_pwm(angle_deg, a, b):
    # Recebe o ângulo em graus e retorna o PWM correspondente
    return int(a * angle_deg + b)

def calculate_angles(servo_values):
    if len(servo_values) != 4:
        raise ValueError("servo_values deve conter exatamente 4 valores")
    # Converte PWM para ângulo em graus
    angle_0_deg = servo_angle(servo_values[0], a0, b0)
    angle_1_deg = servo_angle(servo_values[1], a1, b1)
    angle_2_deg = servo_angle(servo_values[2], a2, b2)
    angle_3_deg = servo_angle(servo_values[3], a3, b3)
    # Converte graus para radianos para uso nas funções trigonométricas
    angle_0_rad = np.radians(angle_0_deg)
    angle_1_rad = np.radians(angle_1_deg)
    angle_2_rad = np.radians(angle_2_deg)
    angle_3_rad = np.radians(angle_3_deg)
    return angle_0_rad, angle_1_rad, angle_2_rad, angle_3_rad

def calculate_transformation_matrix(pwm1, pwm2, pwm3, pwm4):
    o1, o2, o3, o4 = calculate_angles([pwm1, pwm2, pwm3, pwm4])
    t1 = np.array([[np.cos(o1), -np.sin(o1), 0, 0],
                   [np.sin(o1), np.cos(o1), 0, 0],
                   [0, 0, 1, h],
                   [0, 0, 0, 1]])
    t2 = np.array([[np.cos(o2), -np.sin(o2), 0, 0],
                   [0, 0, -1, 0],
                   [np.sin(o2), np.cos(o2), 0, 0],
                   [0, 0, 0, 1]])
    t3 = np.array([[np.cos(o3), -np.sin(o3), 0, L1],
                   [np.sin(o3), np.cos(o3), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    t4 = np.array([[np.cos(o4), -np.sin(o4), 0, L2],
                   [np.sin(o4), np.cos(o4), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    t5 = np.array([[1, 0, 0, L3],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    transformation_matrix = t1 @ t2 @ t3 @ t4 @ t5
    return transformation_matrix

# Pontos de teste (valores PWM dos servos)
ponto1 = np.array([
    angle_to_pwm(10, a0, b0),  # PWM 0: junta 0 em 10 graus
    angle_to_pwm(20, a1, b1),  # PWM 1: junta 1 em 20 graus
    angle_to_pwm(30, a2, b2),  # PWM 2: junta 2 em 30 graus
    angle_to_pwm(40, a3, b3)   # PWM 3: junta 3 em 40 graus
])
ponto2 = np.array([
    angle_to_pwm(50, a0, b0),
    angle_to_pwm(60, a1, b1),
    angle_to_pwm(70, a2, b2),
    angle_to_pwm(80, a3, b3)
])
ponto3 = np.array([
    angle_to_pwm(90, a0, b0),
    angle_to_pwm(100, a1, b1),
    angle_to_pwm(110, a2, b2),
    angle_to_pwm(120, a3, b3)
])
ponto4 = np.array([
    angle_to_pwm(130, a0, b0),
    angle_to_pwm(140, a1, b1),
    angle_to_pwm(150, a2, b2),
    angle_to_pwm(160, a3, b3)
])

pose1 = calculate_transformation_matrix(*ponto1)
pose2 = calculate_transformation_matrix(*ponto2)
pose3 = calculate_transformation_matrix(*ponto3)
pose4 = calculate_transformation_matrix(*ponto4)

# Tabela de validação dos pontos: PWM, ângulos (graus) e posições (X, Y, Z)
dados = []
pontos = [ponto1, ponto2, ponto3, ponto4]
poses = [pose1, pose2, pose3, pose4]
nomes = ['Ponto 1', 'Ponto 2', 'Ponto 3', 'Ponto 4']
for i in range(4):
    pwm = pontos[i]
    ang_rad = calculate_angles(pwm)
    ang_deg = [np.degrees(a) for a in ang_rad]
    pos = poses[i]
    dados.append({
        'Ponto': nomes[i],
        'PWM 0': pwm[0],
        'PWM 1': pwm[1],
        'PWM 2': pwm[2],
        'PWM 3': pwm[3],
        'Ang 0 (°)': f'{ang_deg[0]:.1f}',
        'Ang 1 (°)': f'{ang_deg[1]:.1f}',
        'Ang 2 (°)': f'{ang_deg[2]:.1f}',
        'Ang 3 (°)': f'{ang_deg[3]:.1f}',
        'X (m)': f'{pos[0,3]:.4f}',
        'Y (m)': f'{pos[1,3]:.4f}',
        'Z (m)': f'{pos[2,3]:.4f}'
    })
df = pd.DataFrame(dados)
print(df)

# Plot workspace do robô (tetraedro real)
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
vertices = np.array([
    [pose1[0,3], pose1[1,3], pose1[2,3]],
    [pose2[0,3], pose2[1,3], pose2[2,3]],
    [pose3[0,3], pose3[1,3], pose3[2,3]],
    [pose4[0,3], pose4[1,3], pose4[2,3]]
])
faces = [
    [0, 1, 2],
    [0, 1, 3],
    [1, 2, 3],
    [2, 0, 3]
]
poly3d = [[vertices[idx] for idx in face] for face in faces]
ax.add_collection3d(art3d.Poly3DCollection(poly3d, facecolors='lime', linewidths=1, edgecolors='k', alpha=0.5))
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='blue', s=60)
for i, v in enumerate(vertices):
    ax.text(v[0], v[1], v[2], nomes[i], color='black', fontsize=10)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Pirâmide de Base Triangular (Tetraedro) - Pontos do Robô')
plt.tight_layout()
plt.show()


