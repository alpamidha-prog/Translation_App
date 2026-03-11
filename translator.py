import threading
import time
import speech_recognition as sr
from deep_translator import GoogleTranslator
import customtkinter as ctk

class VoiceTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Live Voice Translator (EN <-> FI)")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Translation State
        self.is_en_to_fi = ctk.BooleanVar(value=True)
        self.is_listening = False
        
        # UI Elements
        self.setup_ui()
        
        # Speech Recognition Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Background Thread
        self.thread = None

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.label_title = ctk.CTkLabel(self, text="Real-Time Translator", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, pady=(20, 10))

        # Toggle Frame
        self.toggle_frame = ctk.CTkFrame(self)
        self.toggle_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.toggle_frame.grid_columnconfigure((0, 2), weight=1)

        self.label_en = ctk.CTkLabel(self.toggle_frame, text="English (EN)", font=ctk.CTkFont(size=14))
        self.label_en.grid(row=0, column=0, padx=10)

        self.switch_toggle = ctk.CTkSwitch(self.toggle_frame, text="", variable=self.is_en_to_fi, onvalue=True, offvalue=False, command=self.update_status_label)
        self.switch_toggle.grid(row=0, column=1)

        self.label_fi = ctk.CTkLabel(self.toggle_frame, text="Finnish (FI)", font=ctk.CTkFont(size=14))
        self.label_fi.grid(row=0, column=2, padx=10)

        # Translation Area
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(size=14))
        self.textbox.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Control Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start Listening", command=self.toggle_listening, fg_color="#2ECC71", hover_color="#27AE60")
        self.start_button.grid(row=0, column=0, padx=10)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Output", command=self.clear_text, fg_color="#E74C3C", hover_color="#C0392B")
        self.clear_button.grid(row=0, column=1, padx=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="#BDC3C7")
        self.status_label.grid(row=4, column=0, pady=(0, 10))

    def update_status_label(self):
        if self.is_en_to_fi.get():
            self.status_label.configure(text="Direction: EN -> FI")
        else:
            self.status_label.configure(text="Direction: FI -> EN")

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_button.configure(text="Stop Listening", fg_color="#F1C40F", hover_color="#F39C12")
            self.status_label.configure(text="Listening...", text_color="#F1C40F")
            self.thread = threading.Thread(target=self.listen_and_translate, daemon=True)
            self.thread.start()
        else:
            self.is_listening = False
            self.start_button.configure(text="Start Listening", fg_color="#2ECC71", hover_color="#27AE60")
            self.status_label.configure(text="Stopping...", text_color="#BDC3C7")

    def clear_text(self):
        self.textbox.delete("1.0", "end")

    def listen_and_translate(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_listening:
                try:
                    # Capture audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Language Detection/Switching logic
                    is_en = self.is_en_to_fi.get()
                    src_lang = 'en' if is_en else 'fi'
                    dest_lang = 'fi' if is_en else 'en'
                    
                    # Speech to Text
                    text = self.recognizer.recognize_google(audio, language=('en-US' if is_en else 'fi-FI'))
                    
                    if text:
                        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
                        
                        # Update UI (Thread-safe)
                        formatted_text = f"[{src_lang.upper()}] {text}\n[{dest_lang.upper()}] {translated}\n\n"
                        self.after(0, self.update_ui_text, formatted_text)
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.after(0, lambda: self.status_label.configure(text="Could not understand audio", text_color="#E74C3C"))
                except Exception as e:
                    self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="#E74C3C"))
                    break
            
            self.after(0, lambda: self.status_label.configure(text="Ready", text_color="#BDC3C7"))

    def update_ui_text(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")

if __name__ == "__main__":
    app = VoiceTranslatorApp()
    app.mainloop()
