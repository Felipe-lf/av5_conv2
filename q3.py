import numpy as np
import matplotlib.pyplot as plt

P_nom = 37e3                
n_s = 1800                  
n_nom = 1780                
I_0 = 26.4                  
I_nom = 61.9                

I = np.linspace(I_0, 483, 500)

n_I = n_s + ((I - I_0) / (I_nom - I_0)) * (n_nom - n_s)

plt.figure(figsize=(10, 6))
plt.plot(I, n_I, label='Velocidade (rpm)', color='orange')
plt.xlabel('Corrente do Rotor (A)')
plt.ylabel('Velocidade (rpm)')
plt.title('Velocidade x Corrente')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

w_nom = 2 * np.pi * n_nom / 60  
T_nom = P_nom / w_nom           

T_emp = T_nom * ((n_s - n_I) / (n_s - n_nom))

plt.figure(figsize=(10, 6))
plt.plot(n_I, T_emp, label='Torque (Nm)', color='purple')
plt.xlabel('Velocidade (rpm)')
plt.ylabel('Torque (Nm)')
plt.title('Torque x Velocidade')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
