# Documentación Técnica: Ataque DHCP Starvation

## 1. Objetivo del Script
El objetivo de este script desarrollado en Scapy es agotar todas las direcciones IP disponibles en el pool de un servidor DHCP legítimo. Al enviar una ráfaga masiva de paquetes DHCP Discover con direcciones MAC falsificadas, el servidor reserva todas sus IPs para clientes inexistentes, provocando una Denegación de Servicio (DoS) para los hosts legítimos que intenten conectarse a la red.

 

## 2. Topología de Red
La red está compuesta por:
2 routers (R1-DHCP y R2)
2 switches
VLAN 10 (clientes + atacante)
VLAN 20 (red interna)
Enlace punto a punto entre routers

| Segmento | Red           | Máscara         | Descripción          |
| -------- | ------------- | --------------- | -------------------- |
| VLAN 10  | 10.15.29.0/24 | 255.255.255.0   | Clientes + atacante  |
| VLAN 20  | 10.15.30.0/24 | 255.255.255.0   | Red interna          |
| R1 ↔ R2  | 10.15.31.0/30 | 255.255.255.252 | Enlace entre routers |

**Segmento afectado (VLAN 10): 10.15.29.0/24**

<img width="1041" height="445" alt="image" src="https://github.com/user-attachments/assets/dd07430b-6e0c-4c1b-8428-46ddacec3b9e" />


## 3. Parámetros usados en el Script
**RandMAC():** Genera direcciones MAC aleatorias para cada paquete enviado.

**Ether(dst="ff:ff:ff:ff:ff:ff"):** Dirección de difusión (broadcast) para que el paquete llegue a todos los dispositivos del segmento.

**BOOTP(chaddr=random_mac):** Coloca la MAC falsificada dentro del campo de dirección de hardware del cliente.

**DHCP(options=[("message-type", "discover"), "end"]):** Define el paquete como un mensaje de descubrimiento DHCP inicial.

**time.sleep(0.01):** Establece un pequeño retardo para controlar el flujo del ataque.


## 4. Demostración de funcionamiento

Ejecución del Script:

<img width="492" height="84" alt="image" src="https://github.com/user-attachments/assets/7233888d-b828-4925-894e-a6200ed8a42c" />

---

**En el scrip debes expecificar la interfaz que vas a usar** y ya, esto es plug and play

Y el server DHCP se queda seco:

<img width="935" height="843" alt="image" src="https://github.com/user-attachments/assets/a2d66119-fcd7-419c-89c8-c4dd2ece0638" />

---

<img width="903" height="239" alt="image" src="https://github.com/user-attachments/assets/6a3d310d-6bf1-4e3b-8003-311727290b0b" />

## 5. Medidas de Mitigación
Para prevenir este tipo de ataques en una red profesional, se deben implementar las siguientes configuraciones en los switches:

**DHCP Snooping:** 
* Configurar los puertos de los usuarios como untrusted (no confiables).
* Configurar el puerto conectado al servidor DHCP real como trusted (confiable).
* Habilitar el límite de tasa (rate-limit) para paquetes DHCP.

**Port Security:** 
* Limitar la cantidad de direcciones MAC permitidas por puerto físico.

Si el switch detecta más de (por ejemplo) 2 MACs en el puerto del atacante, el puerto se desactiva automáticamente (shutdown).

# VIDEO

https://youtu.be/5vQs_07WC_M
