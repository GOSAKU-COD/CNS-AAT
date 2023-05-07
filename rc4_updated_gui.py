import tkinter as tk
from tkinter import messagebox , font
import random


def key_scheduling(key):
    sched = [i for i in range(256)]
    
    key_length = len(key)
    j = 0
    for i in range(256):
        j = (j + sched[i] + key[i % key_length]) % 256
        
        sched[i], sched[j] = sched[j], sched[i]
        
    return sched


def stream_generation(sched):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + sched[i]) % 256
        
        sched[i], sched[j] = sched[j], sched[i]
        
        yield sched[(sched[i] + sched[j]) % 256]   


def encrypt(text, key):
    text = [ord(char) for char in text]
    key = [ord(char) for char in key]
    
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    
    ciphertext = ''
    for char in text:
        enc = str(hex(char ^ next(key_stream))).upper()[2:].zfill(2)
        ciphertext += enc
        
    return ciphertext


def decrypt(ciphertext, key):
    ciphertext = [int(ciphertext[i:i+2], 16) for i in range(0, len(ciphertext), 2)]
    key = [ord(char) for char in key]
    
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    
    plaintext = ''
    for char in ciphertext:
        dec = str(chr(char ^ next(key_stream)))
        plaintext += dec
    
    return plaintext


def encrypt_button_click():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    ciphertext = encrypt(plaintext, key)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ciphertext)


def decrypt_button_click():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()
    plaintext = decrypt(ciphertext, key)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, plaintext)


# Create the main window
window = tk.Tk()
window.title("RC4 ALGORITHM")

# Create and align labels, entry fields, and buttons
plaintext_label = tk.Label(window, text="Plaintext:", font=("Rockwell", 12),fg="light green", bg="black")
plaintext_label.pack(pady=10)
plaintext_entry = tk.Entry(window, font=("Rockwell", 12))
plaintext_entry.pack()

key_label = tk.Label(window, text="Key:", font=("Rockwell", 12),fg="light green", bg="black")
key_label.pack(pady=10)
key_entry = tk.Entry(window, font=("Rockwell", 12))
key_entry.pack()

ciphertext_label = tk.Label(window, text="Ciphertext:", font=("Rockwell", 12),fg="light green", bg="black")
ciphertext_label.pack(pady=10)
ciphertext_entry = tk.Entry(window, font=("Rockwell", 12))
ciphertext_entry.pack()

encrypt_button = tk.Button(window, text="Encrypt", font=("Rockwell", 12),fg="light green", bg="black", command=encrypt_button_click)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(window, text="Decrypt", font=("Rockwell", 12),fg="light green", bg="black", command=decrypt_button_click)
decrypt_button.pack(pady=10)

result_label = tk.Label(window, text="Result:", font=("Rockwell", 12))
result_label.pack(pady=10)
result_text = tk.Text(window, height=5, width=30, font=("Rockwell", 12, "bold"),fg="light green", bg="black")
result_text.pack()

# Configure window appearance
window.configure(bg="black")
window.resizable(False, False)

# Start the Tkinter event loop
window.mainloop()
