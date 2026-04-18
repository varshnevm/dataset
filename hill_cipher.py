import numpy as np


def mod_inverse(a, m):
    """Return the modular inverse of a under modulo m using extended Euclidean algorithm."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse exists for {a} mod {m}")


def matrix_mod_inverse(matrix, mod):
    """Return the modular inverse of a square matrix under the given modulo."""
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det % mod, mod)

    # Adjugate (transpose of cofactor matrix)
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % mod

    return (det_inv * adjugate) % mod


def text_to_numbers(text):
    """Convert a string to a list of numbers (A=0, B=1, ..., Z=25)."""
    return [ord(ch) - ord('A') for ch in text.upper() if ch.isalpha()]


def numbers_to_text(numbers):
    """Convert a list of numbers back to a string."""
    return ''.join(chr(n % 26 + ord('A')) for n in numbers)


def pad_text(text, block_size):
    """Pad text with 'X' so its length is a multiple of block_size."""
    remainder = len(text) % block_size
    if remainder != 0:
        text += 'X' * (block_size - remainder)
    return text


def encrypt(plaintext, key_matrix):
    """
    Encrypt plaintext using the Hill cipher.

    Args:
        plaintext  : The message to encrypt (letters only).
        key_matrix : A square numpy array used as the encryption key.

    Returns:
        The encrypted ciphertext string.
    """
    block_size = key_matrix.shape[0]
    plaintext = pad_text(''.join(ch for ch in plaintext.upper() if ch.isalpha()), block_size)
    numbers = text_to_numbers(plaintext)

    ciphertext = []
    for i in range(0, len(numbers), block_size):
        block = np.array(numbers[i:i + block_size])
        encrypted_block = key_matrix.dot(block) % 26
        ciphertext.extend(encrypted_block.tolist())

    return numbers_to_text(ciphertext)


def decrypt(ciphertext, key_matrix):
    """
    Decrypt ciphertext using the Hill cipher.

    Args:
        ciphertext : The encrypted message (letters only).
        key_matrix : The square numpy array used as the encryption key.

    Returns:
        The decrypted plaintext string.
    """
    block_size = key_matrix.shape[0]
    numbers = text_to_numbers(ciphertext)
    inverse_key = matrix_mod_inverse(key_matrix, 26)

    plaintext = []
    for i in range(0, len(numbers), block_size):
        block = np.array(numbers[i:i + block_size])
        decrypted_block = inverse_key.dot(block) % 26
        plaintext.extend(decrypted_block.astype(int).tolist())

    return numbers_to_text(plaintext)


if __name__ == "__main__":
    # Example: 2x2 key matrix
    key = np.array([[3, 3],
                    [2, 5]])

    message = "HELLO"

    print(f"Original message : {message}")

    ciphertext = encrypt(message, key)
    print(f"Encrypted        : {ciphertext}")

    decrypted = decrypt(ciphertext, key)
    print(f"Decrypted        : {decrypted}")
