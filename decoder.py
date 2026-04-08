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

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python decoder.py [type] [encoded_text]")
        print("Or run without args for interactive mode.")
        print("\nSupported types:")
        print("- base64: Base64 decoding")
        print("- url: URL decoding")
        print("- hex: Hex to text")
        print("- binary: Binary to text (space-separated 8-bit groups)")
        print("- morse: Morse code (letters separated by space, words by /)")
        print("- caesar: Caesar cipher (brute force all shifts)")
        sys.exit(0)

    if len(sys.argv) == 3:
        code_type = sys.argv[1].lower()
        encoded = sys.argv[2]
    else:
        print("Enter the type of code (base64, url, hex, binary, morse, caesar):")
        code_type = input().strip().lower()
        print("Enter the encoded text:")
        encoded = input().strip()

    if code_type == 'base64':
        print(decode_base64(encoded))
    elif code_type == 'url':
        print(decode_url(encoded))
    elif code_type == 'hex':
        print(decode_hex(encoded))
    elif code_type == 'binary':
        print(decode_binary(encoded))
    elif code_type == 'morse':
        print(decode_morse(encoded))
    elif code_type == 'caesar':
        print(decode_caesar(encoded))
    else:
        print("Unknown code type. Run with --help for options.")

if __name__ == "__main__":
    main()