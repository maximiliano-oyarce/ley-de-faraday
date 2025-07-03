import tkinter as tk
from tkinter import messagebox
from faraday3d import Faraday_3D

class VentanaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ley de Faraday")
        self.root.geometry("400x300")
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        # Título
        titulo = tk.Label(frame, text="Ley de Faraday", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # Botones
        tk.Button(frame, text="Simulación personalizada", 
            command=self.personalizado, width=35).pack(pady=10)
        
        tk.Button(frame, text="Simulación con valores por defecto", 
           command=self.simulacion_por_defecto, width=35).pack(pady=10)

        tk.Button(frame, text="Salir", 
            command=self.root.destroy, width=35).pack(pady=10)
    
    def simulacion_por_defecto(self):
        self.root.withdraw()
        simulacion = Faraday_3D(num_vueltas=1, radio_espira=1, B_max=1, frecuencia=1)
        simulacion.ejecutar_simulacion(duracion=10)

    def personalizado(self):
        ventana = tk.Toplevel(self.root)
        self.root.withdraw()
        ventana.title("Tipo de simulación personalizada")
        ventana.geometry("400x400")

        tk.Label(ventana, text="Simulación personalizada", 
                 font=("Arial", 12, "bold")).pack(pady=10)

        entries = {}
        parametros = {
            'num_vueltas': 0,
            'radio_espira': 0,
            'B_max': 0,
            'frecuencia': 0
        }

        label_text = {
            'num_vueltas': 'Número de vueltas:',
            'radio_espira': 'Radio de la espira (m):',
            'B_max': 'Campo magnético máximo (T):',
            'frecuencia': 'Frecuencia (Hz):'
        }

        # Frame para parámetros
        frame_params = tk.Frame(ventana)
        frame_params.pack(pady=10)

        for key, value in parametros.items():
            tk.Label(frame_params, text=label_text[key]).pack(pady=5)
            entry = tk.Entry(frame_params)
            entry.insert(0, str(value))
            entry.pack()
            entries[key] = entry
        
        def ejecutar():
            try:
                num_vueltas = int(entries['num_vueltas'].get())
                radio_espira = float(entries['radio_espira'].get())
                B_max = float(entries['B_max'].get())
                frecuencia = float(entries['frecuencia'].get())
                ventana.destroy()
                
                simulacion = Faraday_3D(num_vueltas, radio_espira, B_max, frecuencia)
                simulacion.ejecutar_simulacion(duracion=10)

            except ValueError:
                messagebox.showerror("Error", "Valores inválidos")

        tk.Button(ventana, text="Iniciar Simulación", 
                 command=ejecutar,
                 width=25, height=2).pack(pady=20)

def main():
    ventana = VentanaPrincipal()
    ventana.root.mainloop()

if __name__ == "__main__":
    main()