import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec

class Faraday_3D:
    def __init__(self, num_vueltas=1, radio_espira=1.0, B_max=2.0, frecuencia=0.5):
        "Simulación de la Ley de Faraday"
        self.num_vueltas = num_vueltas
        self.radio_espira = radio_espira  # Radio de la espira en metros
        self.area_espira = np.pi * self.radio_espira**2
        
        # Parámetros del campo magnético
        self.B_max = B_max  # Campo magnético máximo
        self.frecuencia = frecuencia  # Frecuencia de oscilación del campo
        self.omega = 2 * np.pi * self.frecuencia  # Frecuencia angular

        # Arrays para almacenar datos
        self.tiempo = []
        self.campo_magnetico = []
        self.flujo_magnetico = []
        self.emf_inducida = []
        
        # Configuración de la figura
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.suptitle(f'Simulación de la Ley de Faraday (N={self.num_vueltas}, r={self.radio_espira:.2f}m, B_max={self.B_max:.1f}T, f={self.frecuencia:.2f}Hz)', fontsize=14)
        
        gs = gridspec.GridSpec(2, 2, width_ratios=[1.2, 1])

        # Crear subplots: 3D para la espira, 2D para los gráficos
        self.ax1 = self.fig.add_subplot(gs[:, 0], projection='3d')  # 3D ocupa ambas filas a la izquierda
        self.ax2 = self.fig.add_subplot(gs[0, 1])  # 2D arriba derecha
        self.ax3 = self.fig.add_subplot(gs[1, 1])  # 2D abajo derecha
        
        # Configurar subplots
        self.setup_plots()
        
    def setup_plots(self):
        # Subplot 1: Animación 3D de la espira y campo magnético
        limite = max(2, self.radio_espira * 2.5)
        self.ax1.set_xlim([-limite, limite])
        self.ax1.set_ylim([-limite, limite])
        self.ax1.set_zlim([-1, 1])
        self.ax1.set_title('Espira Conductora 3D y Campo Magnético')
        self.ax1.set_xlabel('X (m)')
        self.ax1.set_ylabel('Y (m)')
        self.ax1.set_zlabel('Z (m)')
        
        # Crear la espira 3D
        theta = np.linspace(0, 2*np.pi, 100)
        self.espira_x = self.radio_espira * np.cos(theta)
        self.espira_y = self.radio_espira * np.sin(theta)
        self.espira_z = np.zeros_like(theta)
        
        # Dibujar la espira inicial
        self.espira_line, = self.ax1.plot(self.espira_x, self.espira_y, self.espira_z, 'b-', linewidth=4, label='Espira Conductora')
          
        # Añadir múltiples vueltas si hay más de una (limitado para rendimiento)
        if self.num_vueltas > 1:
            self.espiras_adicionales = []
            max_vueltas_visibles = min(self.num_vueltas, 5)  # Máximo 5 vueltas para mejor rendimiento
            for vuelta in range(1, max_vueltas_visibles):
                z_offset = vuelta * 0.05  # Separación entre vueltas
                espira_adicional, = self.ax1.plot(self.espira_x, self.espira_y, self.espira_z + z_offset, 'b-', linewidth=3, alpha=0.7)                                  
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
        "Calcula en función del tiempo"
        return self.B_max * np.cos(self.omega * t)
    
    def calcular_flujo_magnetico(self, B):
        return B * self.area_espira
    
    def calcular_emf_inducida(self, t):
        dB_dt = -self.B_max * self.omega * np.sin(self.omega * t)
        dPhi_dt = self.area_espira * dB_dt
        emf = -self.num_vueltas * dPhi_dt
        return emf
    
    def dibujar_campo_magnetico_3d(self, B, ax):
        collections_to_remove = []
        for collection in ax.collections:
            if hasattr(collection, 'campo_magnetico'):
                collections_to_remove.append(collection)
        for collection in collections_to_remove:
            collection.remove()
        
        x = np.linspace(-1.2, 1.2, 4)
        y = np.linspace(-1.2, 1.2, 4)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # La intensidad del campo determina el tamaño de las flechas
        intensidad = abs(B) / self.B_max
        
        # Solo dibuja vectores si la intensidad es significativa
        if intensidad > 0.05:
            # Vectores de campo magnético (perpendicular al plano de la espira)
            U = np.zeros_like(X)
            V = np.zeros_like(Y)
            W = np.full_like(Z, B * 0.4)
            
            # Determinar color basado en la dirección del campo
            if B > 0:
                color = 'red'  # Campo hacia arriba (+Z)
            else:
                color = 'blue'  # Campo hacia abajo (-Z)
            
            # Dibujar vectores de campo magnético
            campo_collection = ax.quiver(X, Y, Z, U, V, W, 
                                       color=color, alpha=0.7,
                                       arrow_length_ratio=0.15, 
                                       linewidth=1.5)
            campo_collection.campo_magnetico = True

        # Líneas de flujo
        if intensidad > 0.1:
            theta_flujo = np.linspace(0, 2*np.pi, 12)
            color = 'red' if B > 0 else 'blue'

            # Círculos de flujo
            for r in [0.5, 0.8]:
                x_flujo = r * np.cos(theta_flujo)
                y_flujo = r * np.sin(theta_flujo)
                z_flujo = np.zeros_like(theta_flujo)
                flujo_line = ax.plot(x_flujo, y_flujo, z_flujo, 
                                   color=color, alpha=0.4, 
                                   linewidth=1)
                flujo_line[0].campo_magnetico = True
    
    def animacion(self, frame):
        "Función de animación"
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
        
        # Dibujar campo magnético en 3D
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
        
        # Rotar la vista 3D
        if frame % 5 == 0:  # Solo rotar cada 5 frames
            azim = 45 + 15 * np.sin(t * 0.3)
            self.ax1.view_init(elev=20, azim=azim)
        
        # Actualizar gráficos de series de tiempo
        self.line_B.set_data(self.tiempo, self.campo_magnetico)
        self.line_emf.set_data(self.tiempo, self.emf_inducida)
        
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
        
        return [self.line_B, self.line_emf]
    
    def ejecutar_simulacion(self, duracion):
        frames = int(duracion / 0.05)
        
        # Crea la animación
        self.anim = animation.FuncAnimation(
            self.fig, self.animacion, frames=frames, 
            interval=40, blit=False, repeat=True,  # Intervalo reducido para mayor fluidez
            cache_frame_data=False  # No almacenar frames en caché para ahorrar memoria
        )
        
        # Agregar leyenda al primer subplot
        self.ax1.legend([self.espira_line], ['Espira Conductora 3D'], loc='upper left')
        
        # Mostrar ecuaciones de Faraday
        ecuacion_text = (
            "Ley de Faraday 3D:\n"
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
