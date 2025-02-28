# Encrypted Image Viewer & Encryptor

This tool provides a simple way to encrypt and decrypt images using AES encryption. 
It consists of two scripts:

1. **encrypt.py** - Encrypts image files in a directory.
2. **viewer.py** - Decrypts and displays encrypted images in a simple viewer.

This was built for personal use but can be useful for anyone who wants to keep their images secure.

---

## Features
- Encrypts images using AES (EAX mode) for confidentiality.
- Decrypts and displays encrypted images via a GUI.
- Supports image rotation and resizing.
- Simple keyboard controls for navigation.

---

## Dependencies
Before using the tool, install the required dependencies:

```sh
sudo apt-get install python3-tk
pip install pyinstaller pycryptodome Pillow
```

---

## Usage

### Encrypting Images
To encrypt images:

1. Run the script:
   ```sh
   python encrypt.py
   ```
2. Enter an encryption key (16, 24, or 32 bytes long).
3. Provide the input directory containing images.
4. Specify the output directory where encrypted files will be stored.
5. The encrypted files will have a `.enc` extension.

### Viewing Encrypted Images
To view encrypted images:

1. Place the encrypted images in the `encrypted_images` folder (or modify the script to specify another location).
2. Run:
   ```sh
   python viewer.py
   ```
3. Enter the decryption key (must be the same as the one used for encryption).
4. Navigate through images using the left/right arrow keys.
5. Press `Space` to rotate images.

---

## Creating Executables
You can create standalone executables for easier usage:

### Encryptor Executable
```sh
python -m PyInstaller --onefile encrypt.py
```
This will generate an executable in the `dist/` folder.

### Viewer Executable
```sh
python -m PyInstaller --onefile viewer.py
```
This will also generate an executable in the `dist/` folder.

Now you can run `encrypt` and `viewer` without needing Python installed.

---

## Notes
- The key must be exactly **16, 24, or 32 bytes** for AES encryption.
- The encrypted images can only be decrypted with the same key.
- The viewer only works with `.enc` files produced by `encrypt.py`.
- Make sure to **remember your encryption key**, as decryption is impossible without it.

---

## License
This tool is provided as-is. Feel free to use, modify, and share it!
