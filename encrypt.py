#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(key, in_filename, out_filename):
    """
    Encrypts a single file using AES (EAX mode).
    The output file will contain [nonce + tag + ciphertext].
    """
    with open(in_filename, 'rb') as f:
        plaintext = f.read()
    
    # Create AES cipher in EAX mode
    cipher = AES.new(key, AES.MODE_EAX)
    
    # Encrypt and get the authentication tag
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # Write nonce, tag, then the ciphertext
    with open(out_filename, 'wb') as f_out:
        f_out.write(cipher.nonce)  # 16 bytes
        f_out.write(tag)           # 16 bytes
        f_out.write(ciphertext)    # remainder

def main():
    """
    Encrypt all images in a user-specified folder using a user-supplied key 
    and place the encrypted files into a specified output folder.
    """
    
    # Prompt user for a key
    key = input("Enter encryption key (16, 24, or 32 bytes): ").encode()
    if len(key) not in [16, 24, 32]:
        print("Error: Key must be 16, 24, or 32 bytes long.")
        return
    
    # Prompt user for input directory
    input_dir = input("Enter the input directory path: ")
    if not os.path.exists(input_dir):
        print("Error: Input directory does not exist.")
        return
    
    # Prompt user for output directory
    output_dir = input("Enter the output directory path: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            in_path = os.path.join(input_dir, filename)
            
            # Append '.enc' to signify an encrypted file
            out_path = os.path.join(output_dir, filename + '.enc')
            
            encrypt_file(key, in_path, out_path)
            print(f"Encrypted {filename} -> {out_path}")

if __name__ == '__main__':
    main()
