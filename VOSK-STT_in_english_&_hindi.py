# in this code when i click on start after select language then model are start loading...
import tkinter as tk
from PIL import ImageTk, Image
from vosk import Model, KaldiRecognizer
import pyaudio
import threading

is_listening = False
language_selected = False
language = ""
model_path = ""
model = None  # Global variable to hold the model

root = tk.Tk()

def load_model():
    global model, model_path
    model = Model(model_path)

def unload_model():
    global model
    model = None

def start_listening():
    global is_listening, language, model

    if is_listening or not language_selected:
        return

    if model is None:
        load_model()

    if language == "english":
        #output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Listening (English)...\n", "heading")
    elif language == "hindi":
        #output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "मैं सुन रहा हूँ (Hindi)...\n", "heading")

    # Update the GUI to display the "Listening" message
    output_text.update_idletasks()

    is_listening = True
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    # Disable the Start button
    start_button.config(state=tk.DISABLED)

    # Enable the Stop button
    stop_button.config(state=tk.NORMAL)

    def listen():
        global is_listening
        while is_listening:
            data = stream.read(8000)

            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()

                if text[14:-3] == "stop" or text[14:-3] == "Stop":
                    output_text.insert(tk.END, "Dictation Stopped\n", "error")
                    stop_listening()  # Call stop_listening() to stop the listening process
                    break
                if text[14:-3] == "new line" or text[14:-3] == "New line":
                    output_text.insert(tk.END, "\n")
                    continue

                output_text.insert(tk.END, text[14:-3] + " ", "normal")
                output_text.see(tk.END)

    threading.Thread(target=listen).start()

def stop_listening():
    global is_listening
    is_listening = False

    # Clear the text in the output_text widget
    #output_text.delete("1.0", tk.END)

    # Enable the Start button
    start_button.config(state=tk.NORMAL)

    # Disable the Stop button
    stop_button.config(state=tk.DISABLED)

def reset_language():
    global language_selected, language, model
    if is_listening:
        stop_listening()

    language_selected = False
    language = ""

    # Clear the text in the output_text widget
    output_text.delete("1.0", tk.END)

    # Unload the model when resetting the language
    unload_model()

    # Enable the language selection buttons and set relief to RAISED
    english_btn.config(relief=tk.RAISED, state=tk.NORMAL)
    hindi_btn.config(relief=tk.RAISED, state=tk.NORMAL)

def language_selection(selected_language):
    global language_selected, language, model_path
    if is_listening or language_selected:
        return

    language_selected = True
    language = selected_language

    if language == "english":
        model_path = r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\Models\vosk-model-en-in-0.5"
        english_btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        hindi_btn.config(relief=tk.RAISED, state=tk.DISABLED)
    elif language == "hindi":
        model_path = r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\Models\vosk-model-hi-0.22"
        english_btn.config(relief=tk.RAISED, state=tk.DISABLED)
        hindi_btn.config(relief=tk.SUNKEN, state=tk.DISABLED)

root.title("श्रुतलेख")
root.geometry("900x600")
root.wm_iconbitmap(r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\logo1.ico")
root.resizable(True, True)

# Set the background image
image = Image.open(r"C:\Users\himanshu.gupta\Downloads\VOSK\cs\GUI\back5.jpg")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# English Button
english_btn = tk.Button(root, text="English", command=lambda: language_selection("english"), font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
english_btn.place(x=100, y=80, width=100, height=25)

# Hindi Button
hindi_btn = tk.Button(root, text="Hindi", command=lambda: language_selection("hindi"), font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
hindi_btn.place(x=100, y=120, width=100, height=25)

# Start and Stop buttons
start_button_img = ImageTk.PhotoImage(file=r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\mic1.jpg")
start_button = tk.Button(root, command=start_listening, image=start_button_img, bd=0, relief=tk.GROOVE, bg="#FFFFFF")
start_button.place(x=120, y=260, width=50, height=50)

start_label = tk.Label(root, text="Tap to Start", font=("Arial", 10, "bold"), bg="#FFFFFF")
start_label.place(x=100, y=315)

stop_button_img = ImageTk.PhotoImage(file=r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\Stop1.jpg")
stop_button = tk.Button(root, command=stop_listening, image=stop_button_img, bd=1, relief=tk.SOLID, bg="#E6E6E6", state=tk.DISABLED)
stop_button.place(x=100, y=360, width=80, height=40)

# Reset Button
reset_btn = tk.Button(root, text="Reset", command=reset_language, font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
reset_btn.place(x=100, y=160, width=100, height=25)

speech_label = tk.Label(root, text="श्रुतलेख", font=("Arial", 12), bg="#FFFFFF")
speech_label.place(x=110, y=500)

# Output textbox
output_text = tk.Text(root, height=20, width=50)
output_text.grid(row=0, column=1, padx=10, pady=10, rowspan=8, columnspan=5, sticky="nsew")
output_text.config(font=("Nirmala UI", 12), wrap=tk.WORD, relief=tk.SOLID, bd=1, padx=5, pady=5, spacing3=5)

output_text.tag_configure("heading", font=("Courier", 15, "bold"), foreground="#d37e7e")
output_text.tag_configure("normal", font=("Nirmala UI", 12), foreground="black")
output_text.tag_configure("error", font=("Arial", 12, "bold"))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

def update_window(event):
    output_text.place(x=280, y=20, width=root.winfo_width() - 310, height=root.winfo_height() - 40)

root.bind("<Configure>", update_window)
root.mainloop()