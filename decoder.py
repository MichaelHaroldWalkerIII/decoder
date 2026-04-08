# pip install pyinstaller
# pyinstaller --onefile decoder.py

import base64
import urllib.parse
import sys

# Morse code dictionary (standard International Morse Code)
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
    '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&',
    '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-',
    '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@', '...---...': 'SOS'
}

# Reverse Morse code dictionary for encoding
MORSE_CODE_REVERSE = {v: k for k, v in MORSE_CODE_DICT.items() if k != '...---...'}

# ========== DECODE FUNCTIONS ==========

def decode_base64(encoded):
    try:
        return base64.b64decode(encoded).decode('utf-8')
    except Exception as e:
        return f"Error decoding Base64: {str(e)}"

def decode_url(encoded):
    try:
        return urllib.parse.unquote(encoded)
    except Exception as e:
        return f"Error decoding URL: {str(e)}"

def decode_hex(encoded):
    try:
        return bytes.fromhex(encoded).decode('utf-8')
    except Exception as e:
        return f"Error decoding Hex: {str(e)}"

def decode_binary(encoded):
    try:
        binary_list = encoded.split()
        decoded = ''.join(chr(int(b, 2)) for b in binary_list)
        return decoded
    except Exception as e:
        return f"Error decoding Binary: {str(e)}"

def decode_morse(encoded):
    try:
        # Split by '/' for words, space for letters
        words = encoded.split('/')
        decoded_words = []
        for word in words:
            letters = word.strip().split(' ')
            decoded_word = ''.join(MORSE_CODE_DICT.get(letter, '?') for letter in letters if letter)
            decoded_words.append(decoded_word)
        return ' '.join(decoded_words)
    except Exception as e:
        return f"Error decoding Morse: {str(e)}"

def decode_caesar(encoded):
    results = []
    encoded = encoded.lower()
    for shift in range(1, 26):
        decoded = ''
        for char in encoded:
            if char.isalpha():
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decoded += char
        results.append(f"Shift {shift}: {decoded}")
    return "\n".join(results)

# ========== ENCODE FUNCTIONS ==========

def encode_base64(text):
    try:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Error encoding Base64: {str(e)}"

def encode_url(text):
    try:
        return urllib.parse.quote(text)
    except Exception as e:
        return f"Error encoding URL: {str(e)}"

def encode_hex(text):
    try:
        return text.encode('utf-8').hex()
    except Exception as e:
        return f"Error encoding Hex: {str(e)}"

def encode_binary(text):
    try:
        return ' '.join(format(ord(c), '08b') for c in text)
    except Exception as e:
        return f"Error encoding Binary: {str(e)}"

def encode_morse(text):
    try:
        text = text.upper()
        words = text.split(' ')
        encoded_words = []
        for word in words:
            encoded_word = ' '.join(MORSE_CODE_REVERSE.get(char, '?') for char in word)
            encoded_words.append(encoded_word)
        return '/'.join(encoded_words)
    except Exception as e:
        return f"Error encoding Morse: {str(e)}"

def encode_caesar(text, shift=3):
    try:
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result
    except Exception as e:
        return f"Error encoding Caesar: {str(e)}"

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python decoder.py [encode|decode] [type] [text]")
        print("Or run without args for interactive mode.")
        print("\nModes:")
        print("  encode - Convert plain text to encoded format")
        print("  decode - Convert encoded text back to plain text")
        print("\nSupported types:")
        print("  base64 - Base64 encoding/decoding")
        print("  url    - URL encoding/decoding")
        print("  hex    - Hex to text / text to hex")
        print("  binary - Binary to text / text to binary (space-separated 8-bit groups)")
        print("  morse  - Morse code (letters separated by space, words by /)")
        print("  caesar - Caesar cipher (encode: shift 3, decode: brute force all shifts)")
        print("\nExamples:")
        print("  python decoder.py encode base64 \"Hello World\"")
        print("  python decoder.py decode morse \".... . .-.. .-.. ---\"")
        sys.exit(0)

    if len(sys.argv) >= 4:
        mode = sys.argv[1].lower()
        code_type = sys.argv[2].lower()
        text = sys.argv[3]
    elif len(sys.argv) == 3:
        # Backward compatibility: assume decode mode
        mode = 'decode'
        code_type = sys.argv[1].lower()
        text = sys.argv[2]
    else:
        print("Enter mode (encode/decode):")
        mode = input().strip().lower()
        print("Enter the type of code (base64, url, hex, binary, morse, caesar):")
        code_type = input().strip().lower()
        print("Enter the text:")
        text = input().strip()

    if mode not in ('encode', 'decode'):
        print("Unknown mode. Use 'encode' or 'decode'. Run with --help for options.")
        return

    if code_type == 'base64':
        print(encode_base64(text) if mode == 'encode' else decode_base64(text))
    elif code_type == 'url':
        print(encode_url(text) if mode == 'encode' else decode_url(text))
    elif code_type == 'hex':
        print(encode_hex(text) if mode == 'encode' else decode_hex(text))
    elif code_type == 'binary':
        print(encode_binary(text) if mode == 'encode' else decode_binary(text))
    elif code_type == 'morse':
        print(encode_morse(text) if mode == 'encode' else decode_morse(text))
    elif code_type == 'caesar':
        print(encode_caesar(text) if mode == 'encode' else decode_caesar(text))
    else:
        print("Unknown code type. Run with --help for options.")

if __name__ == "__main__":
    main()
