import numpy as np
import matplotlib.pyplot as plt

class LeyFaraday:
    def __init__(self):
        self.mu_0 = 4 * np.pi * 1e-7  # Permeabilidad del vacío (H/m)
        
    def flujo_magnetico(self, B, A, theta=0):
        "Calcula a través de una superficie"
        return B * A * np.cos(theta)
    
    def emf_inducida_basica(self, dB_dt, A, theta=0):
        "Calcula la EMF inducida para un campo magnético variable"
        return -A * np.cos(theta) * dB_dt
    
    def campo_magnetico_senoidal(self, t, B0, omega):
        "Campo magnético que varía senoidalmente con el tiempo"
        return B0 * np.sin(omega * t)
    
    def derivada_campo_senoidal(self, t, B0, omega):
        "Derivada temporal del campo magnético senoidal"
        return B0 * omega * np.cos(omega * t)
    
    def bobina_en_campo_uniforme(self, N, A, B0, omega, t):
        "EMF inducida en una bobina de N vueltas en un campo magnético uniforme variable"
        # Campo magnético variable
        B = self.campo_magnetico_senoidal(t, B0, omega)
        
        # Derivada del campo
        dB_dt = self.derivada_campo_senoidal(t, B0, omega)
        
        # EMF inducida (Ley de Faraday)
        emf = -N * A * dB_dt
        
        return B, emf
    
    def bobina_rotatoria(self, N, A, B, omega, t):
        "EMF inducida en una bobina que rota en un campo magnético constante"
        # Flujo magnético variable debido a la rotación
        flujo = B * A * np.cos(omega * t)
        
        # EMF inducida
        emf = N * B * A * omega * np.sin(omega * t)
        
        return flujo, emf
    
    def solenoide_con_nucleo_movil(self, N, A, L, I, x, v):
        "EMF inducida en un solenoide cuando un núcleo se mueve (usando permeabilidad del vacío)"
        # Inductancia usando solo permeabilidad del vacío
        L_inductancia = (self.mu_0 * N**2 * A) / L
        
        # EMF inducida debido al movimiento del núcleo
        emf = -L_inductancia * v / L  # Aproximación simplificada
        
        return emf
    
    def demo_ley_faraday(self):
        "Demostración completa de la Ley de Faraday con diferentes ejemplos"
        print("=" * 60)
        print("DEMOSTRACIÓN DE LA LEY DE FARADAY EN ELECTROMAGNETISMO")
        print("=" * 60)
        
        # Ejemplo 1: Bobina en campo magnético variable
        print("\n1. BOBINA EN CAMPO MAGNÉTICO VARIABLE")
        print("-" * 40)
        
        N = 20  # Número de vueltas
        A = 0.01  # Área = 1 cm²
        B0 = 1  # Campo magnético de 0.1 T
        f = 60  # Frecuencia de 60 Hz
        omega = 2 * np.pi * f
        
        t = np.linspace(0, 3/f, 1000)  # 3 períodos
        B_vals, emf_vals = self.bobina_en_campo_uniforme(N, A, B0, omega, t)
        
        print(f"Parámetros:")
        print(f"- Número de vueltas: {N}")
        print(f"- Área de cada vuelta: {A*1e4:.1f} cm²")
        print(f"- Campo magnético máximo: {B0} T")
        print(f"- Frecuencia: {f} Hz")
        print(f"- EMF máxima: {np.max(np.abs(emf_vals)):.4f} V")
        
        # Gráfica del Ejemplo 1
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(t, B_vals, 'b-', linewidth=2)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Campo Magnético (T)')
        plt.title('Campo Magnético vs Tiempo')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 2)
        plt.plot(t, emf_vals, 'r-', linewidth=2)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('EMF Inducida (V)')
        plt.title('EMF Inducida vs Tiempo')
        plt.grid(True, alpha=0.3)
        
        # Ejemplo 2: Bobina rotatoria
        print("\n2. BOBINA ROTATORIA EN CAMPO CONSTANTE")
        print("-" * 40)
        
        B_const = 0.5  # Campo constante de 0.5 T
        rpm = 1800  # Revoluciones por minuto
        omega_rot = 2 * np.pi * rpm / 60  # Conversión a rad/s
        
        flujo_vals, emf_rot_vals = self.bobina_rotatoria(N, A, B_const, omega_rot, t)
        
        print(f"Parámetros:")
        print(f"- Campo magnético constante: {B_const} T")
        print(f"- Velocidad de rotación: {rpm} RPM")
        print(f"- EMF máxima: {np.max(np.abs(emf_rot_vals)):.4f} V")
        
        plt.subplot(2, 2, 3)
        plt.plot(t, flujo_vals, 'g-', linewidth=2)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Flujo Magnético (Wb)')
        plt.title('Flujo Magnético vs Tiempo')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 4)
        plt.plot(t, emf_rot_vals, 'm-', linewidth=2)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('EMF Inducida (V)')
        plt.title('EMF en Bobina Rotatoria')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Ejemplo 3: Transformador básico
        print("\n3. PRINCIPIO DEL TRANSFORMADOR")
        print("-" * 40)
        
        N1 = 1000  # Vueltas del primario
        N2 = 100   # Vueltas del secundario
        V1 = 220   # Voltaje del primario (V)
        
        # Relación de transformación
        relacion = N2 / N1
        V2 = V1 * relacion
        
        print(f"Transformador:")
        print(f"- Vueltas del primario: {N1}")
        print(f"- Vueltas del secundario: {N2}")
        print(f"- Voltaje del primario: {V1} V")
        print(f"- Voltaje del secundario: {V2:.1f} V")
        print(f"- Relación de transformación: {relacion:.2f}")
        
        # Ejemplo 4: Cálculos numéricos
        print("\n4. CÁLCULOS ESPECÍFICOS")
        print("-" * 40)
        
        # Flujo magnético
        B_test = 0.2  # Tesla
        A_test = 0.005  # m²
        theta_test = np.pi/6  # 30 grados
        
        flujo = self.flujo_magnetico(B_test, A_test, theta_test)
        print(f"Flujo magnético:")
        print(f"- B = {B_test} T, A = {A_test*1e4} cm², θ = {np.degrees(theta_test):.1f}°")
        print(f"- Φ = {flujo:.6f} Wb")
        
        # EMF inducida
        dB_dt_test = 50  # T/s
        emf_test = self.emf_inducida_basica(dB_dt_test, A_test, theta_test)
        print(f"\nEMF inducida:")
        print(f"- dB/dt = {dB_dt_test} T/s")
        print(f"- ε = {emf_test:.6f} V")
        
        return t, B_vals, emf_vals, flujo_vals, emf_rot_vals

def main():
    # Crear instancia de la clase
    faraday = LeyFaraday()
    
    # Ejecutar demostración principal
    resultados = faraday.demo_ley_faraday()
    
    # Mostrar aplicaciones prácticas
    faraday.aplicacion_practica()
    
    # Mostrar ecuaciones importantes
    print("\n" + "="*60)
    print("ECUACIONES FUNDAMENTALES")
    print("="*60)
    print("\n1. Ley de Faraday:")
    print("   ε = -dΦ/dt = -d(B·A)/dt")
    print("\n2. Flujo magnético:")
    print("   Φ = B·A = B·A·cos(θ)")
    print("\n3. EMF en bobina:")
    print("   ε = -N·dΦ/dt")
    print("\n4. Bobina rotatoria:")
    print("   ε = N·B·A·ω·sin(ωt)")
    print("\n5. Transformador:")
    print("   V₂/V₁ = N₂/N₁")

if __name__ == "__main__":
    main()