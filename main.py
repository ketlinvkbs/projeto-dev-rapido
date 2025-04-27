import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

app = ctk.CTk()
app.title('Interface Imformativa sobre Queimadas')
app.geometry('600x800')
app.configure(fg_color='#0B3D2E')

imagem_fundo = Image.open('fundoqueimadas.jpg')
imagem_fundo = imagem_fundo.resize((600, 800))
fundo = ImageTk.PhotoImage(imagem_fundo)

label_fundo = tk.Label(app, image=fundo)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

def abrir_mapa_calor():
    print('abrir mapa calor')

def abrir_concientizacao():
    print('abrir concientização')

def abrir_quiz():
    print('abrir quiz')

titulo = ctk.CTkLabel(
    app,
    text="Bem Vindo á interface\ninformativa sobre",
    font=("cursive", 24),
    text_color='white',
    fg_color="transparent"
)
titulo.pack(pady=20)

imagem = Image.open('logo queimadas.jpg')
imagem = imagem.resize((200, 200))
foto = ImageTk.PhotoImage(imagem)
logo = tk.Label(
    app, 
    image=foto, 
    bg="#0B3D2E"
)
logo.pack(pady=10)

nome = ctk.CTkLabel(
    app,
    text='Queimadas',
    font=("Georgia", 36, "bold"),
    text_color='white',
    fg_color="transparent"
)
nome.pack(pady=5)

subtitulo = ctk.CTkLabel(
    app,
    text="o que deseja acessar?",
    font=("Georgia", 20,),
    text_color='white',
    fg_color="transparent"
)
subtitulo.pack(pady=5)

btn_mapa = ctk.CTkButton(app, text="mapa de calor", command=abrir_mapa_calor, fg_color="goldenrod")
btn_mapa.pack(pady=10)

btn_consciencia = ctk.CTkButton(app, text="Concientização", command=abrir_concientizacao, fg_color="goldenrod")
btn_consciencia.pack(pady=10)

btn_quiz = ctk.CTkButton(app, text="Quiz", command=abrir_quiz, fg_color="goldenrod")
btn_quiz.pack(pady=10)

app.mainloop()








