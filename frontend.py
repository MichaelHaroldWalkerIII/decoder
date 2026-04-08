import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import decoder

CIPHERS = ['base64', 'url', 'hex', 'binary', 'morse', 'caesar']

CIPHER_INFO = {
    'base64': 'Base64 encoding converts text to ASCII characters\nusing 64-character alphabet (A-Z, a-z, 0-9, +, /).',
    'url': 'URL encoding replaces unsafe ASCII characters with\na "%" followed by two hexadecimal digits.',
    'hex': 'Hexadecimal encoding converts each byte to two\nhexadecimal characters (0-9, A-F).',
    'binary': 'Binary encoding converts each character to 8 bits\n(0s and 1s), space-separated.',
    'morse': 'Morse code uses dots (.) and dashes (-).\nLetters separated by space, words by /. ',
    'caesar': 'Caesar cipher shifts each letter by N positions.\nEncode uses adjustable shift, decode shows all 25 shifts.'
}

class EncoderDecoderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Encoder/Decoder")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 11, 'bold'))
        style.configure('Info.TLabel', font=('Helvetica', 9), foreground='gray')
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Encoder / Decoder", style='Title.TLabel')
        title_label.pack(pady=(0, 15))
        
        # Control panel frame
        control_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cipher selection
        cipher_frame = ttk.Frame(control_frame)
        cipher_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cipher_frame, text="Cipher:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.cipher_var = tk.StringVar(value='base64')
        cipher_combo = ttk.Combobox(cipher_frame, textvariable=self.cipher_var, 
                                     values=CIPHERS, state='readonly', width=15)
        cipher_combo.pack(side=tk.LEFT)
        cipher_combo.bind('<<ComboboxSelected>>', self.on_cipher_change)
        
        # Mode selection (Encode/Decode)
        mode_frame = ttk.Frame(control_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="Mode:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.mode_var = tk.StringVar(value='encode')
        encode_rb = ttk.Radiobutton(mode_frame, text="Encode", variable=self.mode_var, 
                                     value='encode', command=self.on_mode_change)
        encode_rb.pack(side=tk.LEFT, padx=(0, 20))
        
        decode_rb = ttk.Radiobutton(mode_frame, text="Decode", variable=self.mode_var, 
                                     value='decode', command=self.on_mode_change)
        decode_rb.pack(side=tk.LEFT)
        
        # Caesar shift control (initially hidden)
        self.shift_frame = ttk.Frame(control_frame)
        
        ttk.Label(self.shift_frame, text="Shift:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.shift_var = tk.IntVar(value=3)
        self.shift_spinbox = ttk.Spinbox(self.shift_frame, from_=1, to=25, 
                                          textvariable=self.shift_var, width=5)
        self.shift_spinbox.pack(side=tk.LEFT)
        
        # Cipher info label
        self.info_label = ttk.Label(control_frame, text="", style='Info.TLabel', wraplength=500)
        self.info_label.pack(fill=tk.X, pady=(10, 0))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD,
                                                     font=('Consolas', 10))
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.on_text_change)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        convert_btn = ttk.Button(button_frame, text="Convert", command=self.convert)
        convert_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        swap_btn = ttk.Button(button_frame, text="Swap", command=self.swap_input_output)
        swap_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        copy_btn = ttk.Button(button_frame, text="Copy Output", command=self.copy_output)
        copy_btn.pack(side=tk.LEFT)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, wrap=tk.WORD,
                                                      font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Initialize UI state
        self.on_cipher_change()
        
    def on_cipher_change(self, event=None):
        cipher = self.cipher_var.get()
        
        # Show/hide shift control for Caesar
        if cipher == 'caesar':
            self.shift_frame.pack(fill=tk.X, pady=5)
        else:
            self.shift_frame.pack_forget()
        
        # Update info label
        self.info_label.config(text=CIPHER_INFO.get(cipher, ''))
        
    def on_mode_change(self):
        # Auto-convert on mode change if there's input
        pass
        
    def on_text_change(self, event=None):
        # Optional: auto-convert as user types (commented out for performance)
        # self.convert()
        pass
        
    def convert(self):
        cipher = self.cipher_var.get()
        mode = self.mode_var.get()
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            self.output_text.delete("1.0", tk.END)
            return
        
        # Get the appropriate function
        if cipher == 'base64':
            func = decoder.encode_base64 if mode == 'encode' else decoder.decode_base64
        elif cipher == 'url':
            func = decoder.encode_url if mode == 'encode' else decoder.decode_url
        elif cipher == 'hex':
            func = decoder.encode_hex if mode == 'encode' else decoder.decode_hex
        elif cipher == 'binary':
            func = decoder.encode_binary if mode == 'encode' else decoder.decode_binary
        elif cipher == 'morse':
            func = decoder.encode_morse if mode == 'encode' else decoder.decode_morse
        elif cipher == 'caesar':
            if mode == 'encode':
                shift = self.shift_var.get()
                func = lambda t: decoder.encode_caesar(t, shift)
            else:
                func = decoder.decode_caesar
        else:
            return
        
        result = func(text)
        
        # Display result
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        
    def swap_input_output(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        output_text = self.output_text.get("1.0", tk.END).strip()
        
        # Swap the text
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", output_text)
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", input_text)
        
        # Toggle mode
        current_mode = self.mode_var.get()
        self.mode_var.set('decode' if current_mode == 'encode' else 'encode')
        
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        
    def copy_output(self):
        output = self.output_text.get("1.0", tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Copied", "Output copied to clipboard!")


def main():
    root = tk.Tk()
    app = EncoderDecoderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
