import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class HoverTest:
    def __init__(self, root):
        self.root = root
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        
        # Pontos de exemplo
        self.x = np.array([1, 2, 3, 4, 5])
        self.y = np.array([5, 4, 3, 2, 1])
        self.scatter = self.ax.scatter(self.x, self.y, c='red', picker=5)
        
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.canvas.mpl_connect("motion_notify_event", self.hover)
    
    def hover(self, event):
        if event.inaxes == self.ax:
            cont, ind = self.scatter.contains(event)
            if cont:
                idx = ind["ind"][0]
                x, y = self.x[idx], self.y[idx]
                print(f"Hover no ponto {idx}: ({x}, {y})")  # Imprime no terminal
                
                self.annot.xy = (x, y)
                texto = f"Ponto {idx}\n({x}, {y})"
                self.annot.set_text(texto)
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if self.annot.get_visible():
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

root = tk.Tk()
root.geometry("700x500")
root.title("Teste Hover Scatter Plot")

app = HoverTest(root)

root.mainloop()
