#Please Have the ciphertext.txt file in the same folder as this python script
#The plaintext.txt and mapping.json will also appear within the same folder once the program finishes it's process 
import sys
import re
import json
from collections import Counter
# Standard English Letter Frequency 
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJQXZ"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Quadgrams (4-letter patterns) - Heuristic Scoring System
# Source: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/
QUADGRAMS = {
    'THAT': 50, 'THER': 45, 'WITH': 45, 'TION': 45, 'OJEC': 40,
    'JECT': 40, 'IGHT': 35, 'HAVE': 35, 'HICH': 35, 'WHIC': 35,
    'THIS': 35, 'THIN': 35, 'THEY': 35, 'ATIO': 35, 'EVER': 35,
    'FROM': 35, 'OUGH': 30, 'VERE': 30, 'TARY': 30, 'INTE': 30,
    'ENTA': 30, 'ERED': 30, 'SEND': 25, 'DING': 25, 'RECT': 25,
    'ENCE': 25, 'DLIN': 25, 'ANCE': 25, 'NTIA': 25, 'CTIO': 25,
    'EFOR': 25, 'ESTA': 25, 'COMP': 25, 'RATI': 25, 'OFTH': 20,
    'THEP': 20, 'OTHE': 20, 'TTHE': 20, 'DTHE': 20, 'INGT': 20,
    'ETHE': 20, 'NGTO': 20, 'AGAI': 15, 'GAIN': 15, 'CTIN': 15,
    'NOFC': 15, 'OCON': 15, 'ORMA': 15, 'SION': 15, 'UNDE': 15,
    'NDER': 15, 'REST': 15, 'PRES': 15, 'RESE': 15, 'CONS': 15,
    'NSID': 15, 'SIDE': 15, 'IDER': 15, 'LITA': 30, 'ALLY': 30,
    'PROJ': 40, 'HERE': 40, 'OULD': 40,
    'MILI': 30, 'GOOD': 30, 'MENT': 30,
    'BOOK': 60, 'PUBL': 40, 'COPY': 40,
    'ABOU': 40, 'PART': 30, 'AMER': 30
}

TRIGRAMS = {
    'THE': 50, 'AND': 50, 'ING': 50, 'ENT': 45, 'ION': 45,
    'HER': 40, 'FOR': 40, 'THA': 40, 'NTH': 40, 'INT': 40,
    'ERE': 40, 'TIO': 40, 'TER': 40, 'EST': 35, 'ERS': 35,
    'ATI': 35, 'HAT': 35, 'ATE': 35, 'ALL': 35, 'ETH': 35,
    'HES': 30, 'VER': 30, 'HIS': 30, 'OFT': 30, 'ITH': 30,
    'FTH': 30, 'STH': 30, 'OTH': 30, 'RES': 30, 'ONT': 30,
    'PRO': 20, 'ECT': 20, 'GHT': 20, 'YOU': 40, 'ARE': 35
}
def read_file(filename):
    """Reads file and removes non-alphabetic characters"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read().upper()
        return re.sub(r'[^A-Z]', '', data)
    except FileNotFoundError:
        print("Error: ciphertext.txt not found.")
        sys.exit(1)

def decrypt_text(text, key):
    """Applies the substitution key to the text"""
    table = str.maketrans(key)
    return text.translate(table)

def get_score(text):
    """Calculates the score based on N-grams"""
    score = 0
    # Quadgrams 
    for i in range(len(text) - 3):
        chunk = text[i:i+4]
        if chunk in QUADGRAMS:
            score += QUADGRAMS[chunk]
    # Trigrams 
    for i in range(len(text) - 2):
        chunk = text[i:i+3]
        if chunk in TRIGRAMS:
            score += TRIGRAMS[chunk]
    return score

def get_initial_key(text):
    """
    Deterministically creates a starting key based on frequency
    """
    counts = Counter(text)
    #Sort cipher letters by frequency 
    sorted_cipher = [pair[0] for pair in counts.most_common()]
    #Fill in any letters not present in the text
    for char in ALPHABET:
        if char not in sorted_cipher:
            sorted_cipher.append(char)
            
    key = {}
    for i, cipher_char in enumerate(sorted_cipher):
        if i < len(ENGLISH_FREQ_ORDER):
            key[cipher_char] = ENGLISH_FREQ_ORDER[i]
        else:
            key[cipher_char] = 'Z'
    return key

def systematic_swap_optimization(text, start_key):
    """
    Deterministically improves the key by trying every possible swap.
    """
    current_key = start_key.copy()
    current_text = decrypt_text(text, current_key)
    current_score = get_score(current_text)
    
    cipher_letters = list(ALPHABET)
    improved = True
    
    print("Starting Optimization...")
    
    #Keep looping through all pairs until no more improvements can be made
    while improved:
        improved = False
        
        #Try swapping every letter with every other letter (A-B, A-C )
        for i in range(len(cipher_letters)):
            for j in range(i + 1, len(cipher_letters)):
                char1 = cipher_letters[i]
                char2 = cipher_letters[j]
                #Create a temporary key with the swap
                test_key = current_key.copy()
                #Perform swap
                test_key[char1], test_key[char2] = test_key[char2], test_key[char1]
                #Check score
                test_text = decrypt_text(text, test_key)
                new_score = get_score(test_text)
                if new_score > current_score:
                    current_score = new_score
                    current_key = test_key
                    improved = True
                    break 
            if improved: break
            
    return current_key

def main():
    # 1.Load Data
    cipher_text = read_file('ciphertext.txt')
    #2. Initial Guess (Frequency Analysis)
    print("Step 1: Initial Frequency Analysis...")
    key = get_initial_key(cipher_text)
    #3. Optimization
    print("Step 2: Refining the key...")
    final_key = systematic_swap_optimization(cipher_text, key)
    #4. Final Output
    final_text = decrypt_text(cipher_text, final_key)
    #Save files
    with open('plaintext.txt', 'w') as f:
        f.write(final_text)
    with open('mapping.json', 'w') as f:
        json.dump(final_key, f, indent=4, sort_keys=True)
    print("\nDecryption complete.")
    print(f"Plaintext saved to: plaintext.txt")
    print("-" * 40)
    print(f"Preview: {final_text[:80]}...")
if __name__ == "__main__":
    main()