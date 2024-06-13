#in this code model load first then application start run
import tkinter as tk
from PIL import ImageTk, Image
from vosk import Model, KaldiRecognizer
import pyaudio
import threading

is_listening = False
language_selected = ""
active_language = ""
model_english_path = r"C:\Users\himanshu.gupta\Downloads\Models\VOSK\Vosk with Large Files\vosk-model-en-in-0.5"
model_hindi_path = r"C:\Users\himanshu.gupta\Downloads\Models\VOSK\Vosk with Large Files\vosk-model-hi-0.22"
model_english = None
model_hindi = None

root = tk.Tk()
root.title("श्रुतलेख")
root.geometry("900x600")
#root.wm_iconbitmap(r"C:\Users\himanshu.gupta\Downloads\VOSK\VOSK with Large file\logo1.ico")
root.resizable(True, True)

# Load both models at the beginning
model_english = Model(model_english_path)
model_hindi = Model(model_hindi_path)

# Set the background image
image = Image.open(r"C:\Users\himanshu.gupta\Downloads\Projects\GUI\VOSK\First project in CS\GUI\back5.jpg")
background_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def start_listening():
    global is_listening, language_selected, active_language

    if is_listening or not active_language:
        return

    if active_language == "english":
        recognizer = KaldiRecognizer(model_english, 16000)
        output_text.insert(tk.END, "(English)...\n")
    elif active_language == "hindi":
        recognizer = KaldiRecognizer(model_hindi, 16000)
        output_text.insert(tk.END, "(हिन्दी)...\n")
    else:
        return

    # Update the GUI to display the "Listening" message
    output_text.update_idletasks()

    is_listening = True

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    # Disable the Start button
    start_button.config(state=tk.DISABLED)

    # Enable the Stop button
    stop_button.config(state=tk.NORMAL)

    # Update the "Start" label text to "Recording"
    start_label.config(text="⚫Recording", foreground="red")

    def listen():
        global is_listening
        while is_listening:
            data = stream.read(8000)

            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()

                if text[14:-3] == "stop" or text[14:-3] == "Stop":
                    output_text.insert(tk.END, "Dictation Stopped\n")
                    stop_listening()  # Call stop_listening() to stop the listening process
                    break
                if text[14:-3] == "new line" or text[14:-3] == "New line":
                    output_text.insert(tk.END, "\n")
                    continue

                output_text.insert(tk.END, text[14:-3] + " ")
                output_text.see(tk.END)

    threading.Thread(target=listen).start()

def stop_listening():
    global is_listening

    is_listening = False

    # Enable the Start button
    start_button.config(state=tk.NORMAL)

    # Disable the Stop button
    stop_button.config(state=tk.DISABLED)

    # Update the "Start" label text to "Tap to Start"
    start_label.config(text="Tap to Start", foreground='black')

def reset_language():
    global language_selected, active_language

    if is_listening:
        stop_listening()

    active_language = ""
    # Clear the text in the output_text widget
    output_text.delete("1.0", tk.END)

    # Enable the language selection buttons and set relief to RAISED
    english_btn.config(relief=tk.RAISED, state=tk.NORMAL)
    hindi_btn.config(relief=tk.RAISED, state=tk.NORMAL)

def language_selection(selected_language):
    global language_selected, active_language

    if is_listening:
        stop_listening()

    active_language = selected_language

    if active_language == "english":
        english_btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        hindi_btn.config(relief=tk.RAISED, state=tk.NORMAL)
    elif active_language == "hindi":
        hindi_btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
        english_btn.config(relief=tk.RAISED, state=tk.NORMAL)

    # Automatically start listening in the new language if it was previously started
    if is_listening:
        start_listening()

# English Button
english_btn = tk.Button(root, text="English", command=lambda: language_selection("english"), font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
english_btn.place(x=100, y=80, width=100, height=25)

# Hindi Button
hindi_btn = tk.Button(root, text="Hindi", command=lambda: language_selection("hindi"), font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
hindi_btn.place(x=100, y=120, width=100, height=25)

# Start and Stop buttons
start_button_img = ImageTk.PhotoImage(file=r"C:\Users\himanshu.gupta\Downloads\Projects\GUI\VOSK\VOSK with Large file\mic1.jpg")
start_button = tk.Button(root, command=start_listening, image=start_button_img, bd=0, relief=tk.GROOVE, bg="#FFFFFF")
start_button.place(x=120, y=260, width=50, height=50)

start_label = tk.Label(root, text="Tap to Start", font=("Arial", 10, "bold"), bg="#FFFFFF")
start_label.place(x=100, y=315)

stop_button_img = ImageTk.PhotoImage(file=r"C:\Users\himanshu.gupta\Downloads\Projects\GUI\VOSK\VOSK with Large file\Stop1.jpg")
stop_button = tk.Button(root, command=stop_listening, image=stop_button_img, bd=1, relief=tk.SOLID, bg="#E6E6E6", state=tk.DISABLED)
stop_button.place(x=105, y=360, width=80, height=40)

# Reset Button
reset_btn = tk.Button(root, text="Reset", command=reset_language, font=("Arial", 10), bd=1, relief=tk.RAISED, activebackground="#e5e5e5")
reset_btn.place(x=100, y=160, width=100, height=25)

speech_label = tk.Label(root, text="श्रुतलेख", font=("Arial", 12), bg="#FFFFFF")
speech_label.place(x=110, y=500)

# Output text box
output_text = tk.Text(root, height=20, width=50, wrap=tk.WORD)
output_text.config(font=("Nirmala UI", 12), relief=tk.SOLID, bd=1, spacing3=5)

output_text.grid(row=0, column=1, padx=10, pady=10, rowspan=8, columnspan=5, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

def update_window(event):
    output_text.place(x=280, y=20, width=root.winfo_width() - 310, height=root.winfo_height() - 40)

root.bind("<Configure>", update_window)
root.mainloop()
