import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
import math

class FaradaySimulation:
    def __init__(self, num_vueltas=1):
        """
        Simulación de la Ley de Faraday
        
        La Ley de Faraday establece que:
        ε = -N * dΦ/dt
        
        Donde:
        ε = Fuerza electromotriz inducida (EMF)
        N = Número de vueltas de la espira
        Φ = Flujo magnético
        dΦ/dt = Cambio del flujo magnético con respecto al tiempo
        """
        self.num_vueltas = num_vueltas
        self.radio_espira = 1.0  # Radio de la espira en metros
        self.area_espira = np.pi * self.radio_espira**2
        
        # Parámetros del campo magnético
        self.B_max = 2.0  # Tesla - Campo magnético máximo
        self.frecuencia = 0.5  # Hz - Frecuencia de oscilación del campo
        self.omega = 2 * np.pi * self.frecuencia  # Frecuencia angular
        
        # Arrays para almacenar datos
        self.tiempo = []
        self.campo_magnetico = []
        self.flujo_magnetico = []
        self.emf_inducida = []
        
        # Configuración de la figura
        self.fig = plt.figure(figsize=(18, 6))
        self.fig.suptitle(f'Simulación de la Ley de Faraday (N = {self.num_vueltas} vueltas)', fontsize=16)
        
        # Crear subplots: 3D para la espira, 2D para los gráficos
        self.ax1 = self.fig.add_subplot(131, projection='3d')
        self.ax2 = self.fig.add_subplot(132)
        self.ax3 = self.fig.add_subplot(133)
        
        # Configurar subplots
        self.setup_plots()
        
    def setup_plots(self):
        """Configurar los gráficos"""
        # Subplot 1: Animación 3D de la espira y campo magnético
        self.ax1.set_xlim([-2, 2])
        self.ax1.set_ylim([-2, 2])
        self.ax1.set_zlim([-1, 1])
        self.ax1.set_title('Espira Conductora 3D y Campo Magnético')
        self.ax1.set_xlabel('X (m)')
        self.ax1.set_ylabel('Y (m)')
        self.ax1.set_zlabel('Z (m)')
        
        # Crear la espira 3D (círculo en el plano XY)
        theta = np.linspace(0, 2*np.pi, 100)
        self.espira_x = self.radio_espira * np.cos(theta)
        self.espira_y = self.radio_espira * np.sin(theta)
        self.espira_z = np.zeros_like(theta)
        
        # Dibujar la espira inicial
        self.espira_line, = self.ax1.plot(self.espira_x, self.espira_y, self.espira_z, 
                                         'b-', linewidth=4, label='Espira Conductora')
        
        # Añadir múltiples vueltas si hay más de una (limitado para rendimiento)
        if self.num_vueltas > 1:
            self.espiras_adicionales = []
            max_vueltas_visibles = min(self.num_vueltas, 5)  # Máximo 5 vueltas para mejor rendimiento
            for vuelta in range(1, max_vueltas_visibles):
                z_offset = vuelta * 0.05  # Separación entre vueltas
                espira_adicional, = self.ax1.plot(self.espira_x, self.espira_y, 
                                                 self.espira_z + z_offset, 
                                                 'b-', linewidth=3, alpha=0.7)
                self.espiras_adicionales.append(espira_adicional)
        
        # Configurar vista 3D
        self.ax1.view_init(elev=20, azim=45)
        
        # Subplot 2: Campo magnético vs tiempo
        self.ax2.set_title('Campo Magnético vs Tiempo')
        self.ax2.set_xlabel('Tiempo (s)')
        self.ax2.set_ylabel('Campo Magnético B (T)')
        self.ax2.grid(True, alpha=0.3)
        self.line_B, = self.ax2.plot([], [], 'r-', linewidth=2, label='B(t)')
        self.ax2.legend()
        
        # Subplot 3: EMF inducida vs tiempo
        self.ax3.set_title('EMF Inducida vs Tiempo')
        self.ax3.set_xlabel('Tiempo (s)')
        self.ax3.set_ylabel('EMF Inducida ε (V)')
        self.ax3.grid(True, alpha=0.3)
        self.line_emf, = self.ax3.plot([], [], 'g-', linewidth=2, label='ε(t)')
        self.ax3.legend()
        
        # Texto para mostrar valores actuales
        self.text_values = self.ax2.text(0.02, 0.98, '', fontsize=10, 
                                       transform=self.ax2.transAxes, verticalalignment='top',
                                       bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
    def calcular_campo_magnetico(self, t):
        """Calcular el campo magnético en función del tiempo"""
        return self.B_max * np.cos(self.omega * t)
    
    def calcular_flujo_magnetico(self, B):
        """Calcular el flujo magnético Φ = B · A"""
        return B * self.area_espira
    
    def calcular_emf_inducida(self, t):
        """Calcular la EMF inducida usando la ley de Faraday"""
        # dΦ/dt = d(B·A)/dt = A·dB/dt
        # dB/dt para B(t) = B_max * cos(ωt) es: -B_max * ω * sin(ωt)
        dB_dt = -self.B_max * self.omega * np.sin(self.omega * t)
        dPhi_dt = self.area_espira * dB_dt
        emf = -self.num_vueltas * dPhi_dt
        return emf
    
    def dibujar_campo_magnetico_3d(self, B, ax):
        """Dibujar las líneas de campo magnético en 3D - Versión optimizada"""
        # Limpiar solo los elementos del campo magnético anterior
        collections_to_remove = []
        for collection in ax.collections:
            if hasattr(collection, 'campo_magnetico'):
                collections_to_remove.append(collection)
        for collection in collections_to_remove:
            collection.remove()
        
        # Reducir la densidad de vectores para mejor rendimiento
        x = np.linspace(-1.2, 1.2, 4)  # Menos puntos para mejor rendimiento
        y = np.linspace(-1.2, 1.2, 4)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # La intensidad del campo determina el tamaño de las flechas
        intensidad = abs(B) / self.B_max
        
        # Solo dibujar vectores si la intensidad es significativa
        if intensidad > 0.05:
            # Vectores de campo magnético (perpendicular al plano de la espira)
            U = np.zeros_like(X)  # Componente X del campo
            V = np.zeros_like(Y)  # Componente Y del campo
            W = np.full_like(Z, B * 0.4)  # Componente Z del campo (perpendicular)
            
            # Determinar color basado en la dirección del campo
            if B > 0:
                color = 'red'  # Campo hacia arriba (+Z)
            else:
                color = 'blue'  # Campo hacia abajo (-Z)
            
            # Dibujar vectores de campo magnético con menos detalle pero más rápido
            campo_collection = ax.quiver(X, Y, Z, U, V, W, 
                                       color=color, alpha=0.7,
                                       arrow_length_ratio=0.15, 
                                       linewidth=1.5)
            campo_collection.campo_magnetico = True
        
        # Simplificar las líneas de flujo - solo mostrar algunas
        if intensidad > 0.1:
            theta_flujo = np.linspace(0, 2*np.pi, 12)  # Menos puntos
            color = 'red' if B > 0 else 'blue'
            
            # Solo dos círculos de flujo en lugar de tres
            for r in [0.5, 0.8]:
                x_flujo = r * np.cos(theta_flujo)
                y_flujo = r * np.sin(theta_flujo)
                z_flujo = np.zeros_like(theta_flujo)
                flujo_line = ax.plot(x_flujo, y_flujo, z_flujo, 
                                   color=color, alpha=0.4, 
                                   linewidth=1)
                flujo_line[0].campo_magnetico = True
    
    def animate(self, frame):
        """Función de animación optimizada"""
        t = frame * 0.05  # Incremento de tiempo
        
        # Calcular valores físicos
        B = self.calcular_campo_magnetico(t)
        Phi = self.calcular_flujo_magnetico(B)
        emf = self.calcular_emf_inducida(t)
        
        # Almacenar datos
        self.tiempo.append(t)
        self.campo_magnetico.append(B)
        self.flujo_magnetico.append(Phi)
        self.emf_inducida.append(emf)
        
        # Dibujar campo magnético en 3D solo cada pocos frames para mejor rendimiento
        if frame % 2 == 0:  # Solo actualizar el campo cada 2 frames
            self.dibujar_campo_magnetico_3d(B, self.ax1)
        
        # Actualizar el color de la espira basado en la EMF inducida
        intensidad_emf = abs(emf) / (self.num_vueltas * self.B_max * self.omega * self.area_espira)
        if emf > 0:
            color_espira = plt.cm.Greens(0.5 + 0.5 * intensidad_emf)
        else:
            color_espira = plt.cm.Oranges(0.5 + 0.5 * intensidad_emf)
        
        self.espira_line.set_color(color_espira)
        
        # Actualizar espiras adicionales si existen
        if hasattr(self, 'espiras_adicionales'):
            for espira_adicional in self.espiras_adicionales:
                espira_adicional.set_color(color_espira)
        
        # Rotar la vista 3D más lentamente para mejor rendimiento
        if frame % 5 == 0:  # Solo rotar cada 5 frames
            azim = 45 + 15 * np.sin(t * 0.3)  # Rotación más lenta y suave
            self.ax1.view_init(elev=20, azim=azim)
        
        # Actualizar gráficos de series de tiempo
        self.line_B.set_data(self.tiempo, self.campo_magnetico)
        self.line_emf.set_data(self.tiempo, self.emf_inducida)
        
        # Optimizar el ajuste de límites - hacerlo menos frecuentemente
        if len(self.tiempo) > 10 and frame % 10 == 0:  # Solo cada 10 frames
            tiempo_max = max(self.tiempo)
            if tiempo_max > 0:
                self.ax2.set_xlim(0, tiempo_max)
            
            # Solo ajustar ylim si hay variación significativa
            if len(set(self.campo_magnetico)) > 1:
                B_min, B_max = min(self.campo_magnetico), max(self.campo_magnetico)
                if abs(B_max - B_min) > 0.001:
                    self.ax2.set_ylim(B_min * 1.1, B_max * 1.1)
            
            self.ax3.set_xlim(0, tiempo_max)
            if self.emf_inducida and len(set(self.emf_inducida)) > 1:
                emf_min, emf_max = min(self.emf_inducida), max(self.emf_inducida)
                if abs(emf_max - emf_min) > 0.001:
                    self.ax3.set_ylim(emf_min * 1.1, emf_max * 1.1)
        
        # Actualizar texto menos frecuentemente
        if frame % 3 == 0:  # Solo cada 3 frames
            azim = 45 + 15 * np.sin(t * 0.3)
            texto = f'Tiempo: {t:.2f} s\n'
            texto += f'Campo B: {B:.3f} T\n'
            texto += f'Flujo Φ: {Phi:.3f} Wb\n'
            texto += f'EMF ε: {emf:.3f} V\n'
            texto += f'Vueltas: {self.num_vueltas}\n'
            texto += f'Vista: {azim:.1f}°'
            self.text_values.set_text(texto)
        
        return [self.line_B, self.line_emf]  # Devolver menos elementos para blit optimizado
    
    def ejecutar_simulacion(self, duracion=10):
        """Ejecutar la simulación optimizada"""
        frames = int(duracion / 0.05)
        
        # Crear animación con configuración optimizada
        self.anim = animation.FuncAnimation(
            self.fig, self.animate, frames=frames, 
            interval=40, blit=False, repeat=True,  # Intervalo reducido para mayor fluidez
            cache_frame_data=False  # No almacenar frames en caché para ahorrar memoria
        )
        
        # Agregar leyenda al primer subplot
        self.ax1.legend([self.espira_line], ['Espira Conductora 3D'], loc='upper left')
        
        # Mostrar ecuaciones de Faraday
        ecuacion_text = (
            "Ley de Faraday 3D (Optimizada):\n"
            "ε = -N × dΦ/dt\n"
            f"ε = -{self.num_vueltas} × d(B×A)/dt\n"
            f"A = π×r² = {self.area_espira:.3f} m²\n"
            "Campo B ⊥ plano espira\n"
            "Renderizado optimizado para tiempo real"
        )
        self.fig.text(0.02, 0.02, ecuacion_text, fontsize=10, 
                     bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.tight_layout()
        plt.show()

def main():
    """Función principal del programa"""
    print("=== SIMULACIÓN DE LA LEY DE FARADAY ===")
    print()
    print("La Ley de Faraday establece que la fuerza electromotriz inducida (EMF)")
    print("en una espira es proporcional al cambio del flujo magnético con el tiempo:")
    print("ε = -N × dΦ/dt")
    print()
    
    # Solicitar entrada del usuario
    while True:
        try:
            num_vueltas = int(input("Ingrese el número de vueltas de la espira (entero positivo): "))
            if num_vueltas > 0:
                break
            else:
                print("Por favor, ingrese un número entero positivo.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
    
    print(f"\nCreando simulación con {num_vueltas} vueltas...")
    print("\nLa animación mostrará:")
    print("- Izquierda: Espira conductora 3D con campo magnético variable")
    print("- Centro: Campo magnético B(t) vs tiempo")
    print("- Derecha: EMF inducida ε(t) vs tiempo")
    print("\nNota: El campo magnético cambia sinusoidalmente perpendicular al plano.")
    print("      Vectores rojos = campo hacia arriba (+Z)")
    print("      Vectores azules = campo hacia abajo (-Z)")
    print("      La espira cambia de color según la EMF inducida")
    print("      La vista 3D rota suavemente para mejor visualización")
    print("\nOptimizaciones aplicadas para tiempo real:")
    print("- Reducción de densidad de vectores de campo magnético")
    print("- Actualización selectiva de elementos gráficos por frames")
    print("- Rotación de vista más lenta y suave")
    print("- Límite en el número de vueltas visibles (máx. 5)")
    print("- Intervalo de animación optimizado (40ms)")
    print("- Renderizado optimizado sin almacenamiento en caché")
    print("\n¡Cerrando la ventana se terminará la simulación!")
    
    # Crear y ejecutar la simulación
    simulacion = FaradaySimulation(num_vueltas)
    simulacion.ejecutar_simulacion(duracion=20)  # 20 segundos de simulación

if __name__ == "__main__":
    main()