# Heuristic-Cipher-Breaker
A Python tool designed to crack Monoalphabetic Substitution Ciphers without a key. It uses statistical frequency analysis and n-gram scoring (Trigrams/Quadgrams) to heuristically determine the original plaintext.

## 🔓 How It Works

1.  **Frequency Analysis**: It makes an initial guess by matching the frequency of letters in the ciphertext to the standard English frequency order (`ETAOIN...`).
2.  **Heuristic Optimization**: It uses a "Hill Climbing" approach. It systematically swaps letters in the key, decrypts the text, and checks if the new text looks "more English" using a scoring system based on common 3-letter and 4-letter patterns (e.g., `THE`, `AND`, `TION`, `WITH`).
3.  **Result**: It outputs the decrypted text and the discovered key mapping.

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* No external libraries required (uses standard `sys`, `re`, `json`, `collections`).

### Setup & Usage

1.  **Prepare the Ciphertext**:
    Create a file named `ciphertext.txt` in the same folder as the script. Paste your encrypted text inside it.

2.  **Run the Solver**:
    Open your terminal and run:
    ```bash
    python solve.py
    ```

3.  **View Results**:
    Once the optimization finishes, two new files will appear:
    * `plaintext.txt`: The decrypted readable text.
    * `mapping.json`: The specific key used to decrypt it (Cipher Letter -> Plain Letter).

## 📂 File Structure

* **`solve.py`**: The main logic script.
* **`ciphertext.txt`**: (Input) The encrypted text you want to break.
* **`plaintext.txt`**: (Output) The resulting decrypted text.
* **`mapping.json`**: (Output) A JSON file showing which ciphertext letter corresponds to which English letter.

## ⚠️ Limitations

* **Language**: This tool is hardcoded for **English** text only.
* **Text Length**: The algorithm relies on statistics. It works best on texts longer than 100 characters. Very short messages may not have enough data to be cracked accurately.
* **Local Optima**: Sometimes the solver might get "stuck" on a mostly correct solution but miss a few rare letters (like J, Q, or Z).

## 🧠 Scoring Heuristics
The accuracy is driven by a weighted scoring system of common English patterns, including:
* **Quadgrams**: `THAT`, `THER`, `WITH`, `TION`...
* **Trigrams**: `THE`, `AND`, `ING`, `ENT`...

