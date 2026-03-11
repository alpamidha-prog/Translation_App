import threading
import time
import speech_recognition as sr
from deep_translator import GoogleTranslator
import customtkinter as ctk
import cv2
from PIL import Image

class VoiceTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VoiceFlow - AI Translator (EN <-> FI)")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Application State
        self.is_en_to_fi = ctk.BooleanVar(value=True)
        self.is_listening = False
        self.is_camera_on = False
        
        # UI Elements
        self.setup_ui()
        
        # Speech Recognition Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Threads
        self.listen_thread = None
        self.camera_thread = None

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header with Red Theme Style
        self.label_title = ctk.CTkLabel(self, text="VoiceFlow", font=ctk.CTkFont(size=32, weight="bold"), text_color="#ff416c")
        self.label_title.grid(row=0, column=0, pady=(30, 10))

        # Toggle Frame
        self.toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.toggle_frame.grid(row=1, column=0, pady=10, padx=20)
        
        self.label_en = ctk.CTkLabel(self.toggle_frame, text="English", font=ctk.CTkFont(size=14))
        self.label_en.grid(row=0, column=0, padx=15)

        self.switch_toggle = ctk.CTkSwitch(self.toggle_frame, text="", variable=self.is_en_to_fi, onvalue=True, offvalue=False, progress_color="#ef4444", command=self.update_status_label)
        self.switch_toggle.grid(row=0, column=1)

        self.label_fi = ctk.CTkLabel(self.toggle_frame, text="Finnish", font=ctk.CTkFont(size=14))
        self.label_fi.grid(row=0, column=2, padx=15)

        # Translation Area
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(size=15), border_width=1, border_color="#334155")
        self.textbox.grid(row=2, column=0, padx=40, pady=20, sticky="nsew")

        # Control Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, pady=(0, 30))

        self.start_button = ctk.CTkButton(self.button_frame, text="Start Listening", command=self.toggle_listening, fg_color="#ef4444", hover_color="#ff416c", font=ctk.CTkFont(weight="bold"))
        self.start_button.grid(row=0, column=0, padx=10)

        self.camera_button = ctk.CTkButton(self.button_frame, text="Open Camera", command=self.toggle_camera, fg_color="#334155", hover_color="#475569", font=ctk.CTkFont(weight="bold"))
        self.camera_button.grid(row=0, column=1, padx=10)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear", command=self.clear_text, fg_color="transparent", border_width=1, border_color="#334155")
        self.clear_button.grid(row=0, column=2, padx=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="#94a3b8")
        self.status_label.grid(row=4, column=0, pady=(0, 20))

    def update_status_label(self):
        if self.is_en_to_fi.get():
            self.status_label.configure(text="Direction: EN -> FI")
        else:
            self.status_label.configure(text="Direction: FI -> EN")

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.start_button.configure(text="Stop Listening", fg_color="#ff4b2b")
            self.status_label.configure(text="Listening...", text_color="#ef4444")
            self.listen_thread = threading.Thread(target=self.listen_and_translate, daemon=True)
            self.listen_thread.start()
        else:
            self.is_listening = False
            self.start_button.configure(text="Start Listening", fg_color="#ef4444")
            self.status_label.configure(text="Stopping...")

    def toggle_camera(self):
        if not self.is_camera_on:
            self.is_camera_on = True
            self.camera_button.configure(text="Close Camera", fg_color="#ff4b2b")
            self.camera_thread = threading.Thread(target=self.camera_preview, daemon=True)
            self.camera_thread.start()
        else:
            self.is_camera_on = False
            self.camera_button.configure(text="Open Camera", fg_color="#334155")

    def camera_preview(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.after(0, lambda: self.status_label.configure(text="Error: Could not open camera"))
            self.is_camera_on = False
            return

        while self.is_camera_on:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Show the frame in a separate window
            cv2.imshow("VoiceFlow Camera Preview", frame)
            
            # Add a slight delay and check for 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_camera_on = False
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.after(0, lambda: self.camera_button.configure(text="Open Camera", fg_color="#334155"))

    def clear_text(self):
        self.textbox.delete("1.0", "end")

    def listen_and_translate(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    is_en = self.is_en_to_fi.get()
                    src_lang = 'en' if is_en else 'fi'
                    dest_lang = 'fi' if is_en else 'en'
                    
                    text = self.recognizer.recognize_google(audio, language=('en-US' if is_en else 'fi-FI'))
                    
                    if text:
                        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
                        formatted_text = f"[{src_lang.upper()}] {text}\n[{dest_lang.upper()}] {translated}\n\n"
                        self.after(0, self.update_ui_text, formatted_text)
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="#ef4444"))
                    break
            
            self.after(0, lambda: self.status_label.configure(text="Ready", text_color="#94a3b8"))

    def update_ui_text(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")

if __name__ == "__main__":
    app = VoiceTranslatorApp()
    app.mainloop()

