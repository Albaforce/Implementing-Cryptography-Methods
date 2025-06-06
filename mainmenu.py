#!/usr/bin/env python3
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.markdown import Markdown
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import hashlib
import random
import sympy
from typing import Tuple, Optional

# Import cryptographic modules (adjust imports based on your actual structure)
sys.path.append(".")  # Add current directory to path

# Symmetric encryption
try:
    from chiffrement.symetrique.main import main as symmetric_main
    from chiffrement.symetrique.main import (
        cesar_encrypt, cesar_decrypt,
        substitution_encrypt, substitution_decrypt,
        affine_encrypt, affine_decrypt,
        hill_encrypt, hill_decrypt,
        playfair_encrypt, playfair_decrypt,
        vigenere_encrypt, vigenere_decrypt,
        block_cipher_encrypt, block_cipher_decrypt,
        stream_cipher_encrypt, stream_cipher_decrypt,
        des_encrypt, des_decrypt,
        triple_des_encrypt, triple_des_decrypt,
        desx_encrypt, desx_decrypt
    )
except ImportError:
    symmetric_main = None
    cesar_encrypt = cesar_decrypt = None
    substitution_encrypt = substitution_decrypt = None
    affine_encrypt = affine_decrypt = None
    hill_encrypt = hill_decrypt = None
    playfair_encrypt = playfair_decrypt = None
    vigenere_encrypt = vigenere_decrypt = None
    block_cipher_encrypt = block_cipher_decrypt = None
    stream_cipher_encrypt = stream_cipher_decrypt = None
    des_encrypt = des_decrypt = None
    triple_des_encrypt = triple_des_decrypt = None
    desx_encrypt = desx_decrypt = None

# Asymmetric encryption - Import directly from implementation files
try:
    # For AES
    sys.path.append("./chiffrement/asymetrique")
    from cryptography.hazmat.primitives.asymmetric import dh
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.backends import default_backend
    
    # Import AES functions
    try:
        # Try importing AES_implementation, handle if not found
        from chiffrement.asymetrique.AES_implementation import (
                    aes_encrypt_block, aes_decrypt_block )
    except ImportError:
        aes_encrypt_block = aes_decrypt_block = None
    
    # Import RSA functions
    try:
        from chiffrement.asymetrique.RSA_detailed import (
            generate_keys, encrypt_text, decrypt_text
        )
    except ImportError:
        generate_keys = encrypt_text = decrypt_text = None

except ImportError:
    dh = hashes = HKDF = default_backend = None
    aes_encrypt_block = aes_decrypt_block = None
    generate_keys = encrypt_text = decrypt_text = None

# Hashing
try:
    from hachage.SHA_256 import SHA256
    from hachage.RIPEMD_160 import RIPEMD160
except ImportError:
    SHA256 = RIPEMD160 = None

# Signatures
try:
    from signature.rsa_signature import RSASignature
    from signature.dsa import DSA
    #from signature.elgamal_signature import ElGamalSignature
    from signature.paillier_he import PaillierHE, PaillierPublicKey, PaillierPrivateKey
    from signature.shamir_sss import ShamirSecretSharing
    #from signature.elgamal_signature import ElGamalParams, ElGamalPrivateKey, ElGamalPublicKey

except ImportError as e:
    print(f"Import error: {e}")  # For debugging
    RSASignature = DSA = ElGamalSignature = PaillierHE = ShamirSecretSharing = None
    result = type(e)
    realresult = e
    PaillierPublicKey = PaillierPrivateKey = None
    ElGamalParams = ElGamalPrivateKey = ElGamalPublicKey = None

# Initialize Rich console
console = Console()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the application header."""
    console.print(Panel.fit(
        Markdown("# 🔐 Cryptography Toolkit"),
        border_style="blue",
        padding=(1, 2)
    ))

def get_file_content(file_path):
    """Read file content."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {e}")
        return None

def save_file_content(file_path, content):
    """Save content to file."""
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving file:[/bold red] {e}")
        return False

def encryption_menu():
    """Display encryption menu."""
    clear_screen()
    display_header()
    
    table = Table(title="🔒 Encryption Options")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "Classic Ciphers")
    table.add_row("2", "Modern Symmetric Encryption")
    table.add_row("3", "AES Encryption")
    table.add_row("4", "RSA Encryption")
    table.add_row("5", "Diffie-Hellman Key Exchange")
    table.add_row("0", "Back to Main Menu")
    
    console.print(table)
    
    choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5"], default="0")
    
    if choice == "1":
        handle_classic_encryption()
    elif choice == "2":
        handle_modern_symmetric_encryption()
    elif choice == "3":
        handle_aes_encryption()
    elif choice == "4":
        handle_rsa_encryption()
    elif choice == "5":
        handle_diffie_hellman()
    
    return choice != "0"

def handle_classic_encryption():
    """Handle classic cipher encryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🏛️ Classic Cipher Encryption[/bold]", border_style="cyan"))
    
    if cesar_encrypt is None:
        console.print("[bold red]Classic cipher modules not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    # Create classic cipher submenu
    table = Table(title="Classic Cipher Methods")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Era", style="yellow")
    
    table.add_row("1", "César Cipher", "Ancient Rome")
    table.add_row("2", "Substitution Cipher", "Medieval")
    table.add_row("3", "Affine Cipher", "Classical")
    table.add_row("4", "Hill Cipher", "1929")
    table.add_row("5", "Playfair Cipher", "1854")
    table.add_row("6", "Vigenère Cipher", "1553")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select a cipher", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")
    
    if choice == "0":
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    if input_type == "text":
        plaintext = Prompt.ask("Enter plaintext")
    else:
        file_path = Prompt.ask("Enter input file path")
        plaintext = get_file_content(file_path)
        if not plaintext:
            return
    
    result = ""
    
    try:
        if choice == "1":  # César
            shift = int(Prompt.ask("Enter shift value (integer)", default="3"))
            result = cesar_encrypt(plaintext, shift)
            
        elif choice == "2":  # Substitution
            alphabet = Prompt.ask("Enter substitution alphabet (26 unique letters)", 
                                default="ZYXWVUTSRQPONMLKJIHGFEDCBA")
            result = substitution_encrypt(plaintext, alphabet)
            
        elif choice == "3":  # Affine
            a = int(Prompt.ask("Enter 'a' parameter (must be coprime to 26)", default="5"))
            b = int(Prompt.ask("Enter 'b' parameter", default="8"))
            result = affine_encrypt(plaintext, a, b)
            
        elif choice == "4":  # Hill
            matrix_size = int(Prompt.ask("Enter matrix size", choices=["2", "3"], default="2"))
            matrix = []
            console.print("Enter matrix values row by row:")
            for i in range(matrix_size):
                row = []
                for j in range(matrix_size):
                    val = int(Prompt.ask(f"Enter value for position ({i+1},{j+1})"))
                    row.append(val)
                matrix.append(row)
            result = hill_encrypt(plaintext, matrix)
            
        elif choice == "5":  # Playfair
            key = Prompt.ask("Enter Playfair key", default="MONARCHY")
            result = playfair_encrypt(plaintext, key)
            
        elif choice == "6":  # Vigenère
            key = Prompt.ask("Enter Vigenère key", default="LEMON")
            result = vigenere_encrypt(plaintext, key)
        
        # Display or save the result
        console.print(f"\n[bold green]✅ Encryption successful![/bold green]")
        if input_type == "text":
            console.print(f"[bold cyan]Original text:[/bold cyan] {plaintext}")
            console.print(f"[bold green]Encrypted text:[/bold green] {result}")
        else:
            output_path = Prompt.ask("Enter output file path", default=f"{file_path}.classic_enc")
            if save_file_content(output_path, result):
                console.print(f"[bold green]Encrypted content saved to:[/bold green] {output_path}")
                
    except Exception as e:
        console.print(f"[bold red]❌ Error during encryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def handle_modern_symmetric_encryption():
    """Handle modern symmetric encryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔧 Modern Symmetric Encryption[/bold]", border_style="cyan"))
    
    if block_cipher_encrypt is None:
        console.print("[bold red]Modern symmetric encryption modules not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    # Create modern symmetric encryption submenu
    table = Table(title="Modern Symmetric Encryption Methods")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Type", style="yellow")
    
    table.add_row("1", "Block Cipher", "Block")
    table.add_row("2", "Stream Cipher", "Stream")
    table.add_row("3", "DES", "Block (56-bit)")
    table.add_row("4", "Triple DES (3DES)", "Block (168-bit)")
    table.add_row("5", "DESX", "Block (Enhanced DES)")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select a cipher", choices=["0", "1", "2", "3", "4", "5"], default="0")
    
    if choice == "0":
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    if input_type == "text":
        plaintext = Prompt.ask("Enter plaintext")
    else:
        file_path = Prompt.ask("Enter input file path")
        plaintext = get_file_content(file_path)
        if not plaintext:
            return
    
    result = ""
    
    try:
        if choice == "1":  # Block cipher
            key = Prompt.ask("Enter Block cipher key")
            result = block_cipher_encrypt(plaintext, key)
            
        elif choice == "2":  # Stream cipher
            key = Prompt.ask("Enter Stream cipher key")
            result = stream_cipher_encrypt(plaintext, key)
            
        elif choice == "3":  # DES
            key = Prompt.ask("Enter DES key (8 bytes/64 bits)")
            result = des_encrypt(plaintext, key)
            
        elif choice == "4":  # Triple DES
            console.print("[yellow]Triple DES uses three 64-bit keys[/yellow]")
            key1 = Prompt.ask("Enter first DES key")
            key2 = Prompt.ask("Enter second DES key") 
            key3 = Prompt.ask("Enter third DES key")
            result = triple_des_encrypt(plaintext, key1, key2, key3)
            
        elif choice == "5":  # DESX
            console.print("[yellow]DESX uses DES with pre and post whitening keys[/yellow]")
            key = Prompt.ask("Enter DESX main key")
            key_pre = Prompt.ask("Enter pre-whitening key")
            key_post = Prompt.ask("Enter post-whitening key")
            result = desx_encrypt(plaintext, key, key_pre, key_post)
        
        # Display or save the result
        console.print(f"\n[bold green]✅ Encryption successful![/bold green]")
        if input_type == "text":
            console.print(f"[bold cyan]Original text:[/bold cyan] {plaintext}")
            console.print(f"[bold green]Encrypted text:[/bold green] {result}")
        else:
            output_path = Prompt.ask("Enter output file path", default=f"{file_path}.sym_enc")
            if save_file_content(output_path, result):
                console.print(f"[bold green]Encrypted content saved to:[/bold green] {output_path}")
                
    except Exception as e:
        console.print(f"[bold red]❌ Error during encryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def handle_aes_encryption():
    """Handle AES encryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🛡️ AES Encryption[/bold]", border_style="cyan"))
    
    if aes_encrypt_block is None:
        console.print("[bold red]AES encryption module not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    try:
        if input_type == "text":
            plaintext = Prompt.ask("Enter plaintext")
            
            # Make sure text is exactly 16 bytes (pad if necessary)
            if len(plaintext.encode('utf-8')) != 16:
                plaintext = plaintext.ljust(16)[:16]  # Pad or truncate to 16 bytes
                console.print("[yellow]⚠️ Text adjusted to 16 bytes for AES-128[/yellow]")
            
            key = Prompt.ask("Enter encryption key (16 bytes for AES-128)")
            
            # Make sure key is exactly 16 bytes (pad if necessary)
            if len(key.encode('utf-8')) != 16:
                key = key.ljust(16)[:16]  # Pad or truncate to 16 bytes
                console.print("[yellow]⚠️ Key adjusted to 16 bytes for AES-128[/yellow]")
            
            # Convert to bytes
            plaintext_bytes = plaintext.encode('utf-8')
            key_bytes = key.encode('utf-8')
            
            # Encrypt
            encrypted_bytes = aes_encrypt_block(plaintext_bytes, key_bytes)
            encrypted_hex = encrypted_bytes.hex()
            
            console.print(f"\n[bold green]✅ AES Encryption Complete![/bold green]")
            console.print(f"[bold cyan]Plaintext:[/bold cyan] {plaintext}")
            console.print(f"[bold green]Encrypted (hex):[/bold green] {encrypted_hex}")
        else:
            file_path = Prompt.ask("Enter input file path")
            content = get_file_content(file_path)
            if content:
                # Process file in 16-byte blocks
                key = Prompt.ask("Enter encryption key (16 bytes for AES-128)")
                
                # Make sure key is exactly 16 bytes (pad if necessary)
                if len(key.encode('utf-8')) != 16:
                    key = key.ljust(16)[:16]  # Pad or truncate to 16 bytes
                    console.print("[yellow]⚠️ Key adjusted to 16 bytes for AES-128[/yellow]")
                
                key_bytes = key.encode('utf-8')
                
                # Convert content to bytes if it's not already
                if isinstance(content, str):
                    content_bytes = content.encode('utf-8')
                else:
                    content_bytes = content
                
                # Pad content to a multiple of 16 bytes
                padding = 16 - (len(content_bytes) % 16)
                padded_content = content_bytes + bytes([padding] * padding)
                
                # Encrypt each block
                encrypted_bytes = b''
                for i in range(0, len(padded_content), 16):
                    block = padded_content[i:i+16]
                    encrypted_block = aes_encrypt_block(block, key_bytes)
                    encrypted_bytes += encrypted_block
                
                # Save to file
                output_path = Prompt.ask("Enter output file path", default=f"{file_path}.aes")
                with open(output_path, 'wb') as f:
                    f.write(encrypted_bytes)
                console.print(f"[bold green]✅ Encrypted content saved to:[/bold green] {output_path}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error during AES encryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")


def handle_rsa_encryption():
    """Handle RSA encryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔑 RSA Encryption[/bold]", border_style="cyan"))
    
    if generate_keys is None or encrypt_text is None:
        console.print("[bold red]RSA encryption module not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    try:
        # Generate keys or use existing ones
        key_choice = Prompt.ask("Generate new keys or use existing?", 
                              choices=["generate", "existing"], 
                              default="generate")
        
        if key_choice == "generate":
            bits = int(Prompt.ask("Key size in bits (256 for testing, 1024+ for security)", default="512"))
            e = int(Prompt.ask("Public exponent (usually 65537)", default="65537"))
            
            console.print("[yellow]🔄 Generating RSA keys, please wait...[/yellow]")
            public_key, private_key = generate_keys(bits=bits, e=e)
            
            console.print(f"[bold green]✅ Public Key (n, e):[/bold green] {public_key}")
            console.print(f"[bold green]🔐 Private Key (n, d):[/bold green] {private_key}")
            
            # Option to save keys
            save_keys = Confirm.ask("💾 Save keys to file?")
            if save_keys:
                pub_path = Prompt.ask("Public key file path", default="public_key.txt")
                priv_path = Prompt.ask("Private key file path", default="private_key.txt")
                
                with open(pub_path, 'w') as f:
                    f.write(f"{public_key[0]},{public_key[1]}")
                with open(priv_path, 'w') as f:
                    f.write(f"{private_key[0]},{private_key[1]}")
                
                console.print(f"[bold green]✅ Keys saved to {pub_path} and {priv_path}[/bold green]")
        else:
            # Load existing keys
            pub_path = Prompt.ask("Public key file path")
            with open(pub_path, 'r') as f:
                n, e = map(int, f.read().split(','))
                public_key = (n, e)
            
            console.print(f"[bold green]📂 Loaded public key:[/bold green] {public_key}")
        
        # Encrypt message
        input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
        
        if input_type == "text":
            plaintext = Prompt.ask("Enter plaintext to encrypt")
            
            # Check if message is too long
            max_bytes = (public_key[0].bit_length() // 8) - 11  # Safe byte length for RSA
            if len(plaintext.encode('utf-8')) > max_bytes:
                console.print(f"[bold red]⚠️ Warning: Message is too long for key size![/bold red]")
                console.print(f"[yellow]Max length with this key is {max_bytes} bytes[/yellow]")
                plaintext = plaintext[:max_bytes]
                console.print(f"[yellow]✂️ Message truncated to fit key size[/yellow]")
            
            encrypted = encrypt_text(plaintext, public_key)
            console.print(f"\n[bold green]✅ RSA Encryption Complete![/bold green]")
            console.print(f"[bold cyan]Original text:[/bold cyan] {plaintext}")
            console.print(f"[bold green]Encrypted (base64):[/bold green] {encrypted}")
            
            # Option to save encrypted text
            save_enc = Confirm.ask("💾 Save encrypted text to file?")
            if save_enc:
                enc_path = Prompt.ask("Encrypted file path", default="encrypted.txt")
                with open(enc_path, 'w') as f:
                    f.write(encrypted)
                console.print(f"[bold green]✅ Encrypted text saved to {enc_path}[/bold green]")
        else:
            file_path = Prompt.ask("Enter input file path")
            content = get_file_content(file_path)
            if content:
                # Check if content is too long
                max_bytes = (public_key[0].bit_length() // 8) - 11
                if len(content.encode('utf-8')) > max_bytes:
                    console.print(f"[bold red]⚠️ Warning: File is too long for direct RSA encryption![/bold red]")
                    console.print(f"[yellow]Only the first {max_bytes} bytes will be encrypted[/yellow]")
                    content = content[:max_bytes]
                
                encrypted = encrypt_text(content, public_key)
                output_path = Prompt.ask("Enter output file path", default=f"{file_path}.rsa")
                with open(output_path, 'w') as f:
                    f.write(encrypted)
                console.print(f"[bold green]✅ Encrypted content saved to:[/bold green] {output_path}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error during RSA encryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def handle_diffie_hellman():
    """Handle Diffie-Hellman key exchange."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🤝 Diffie-Hellman Key Exchange[/bold]", border_style="cyan"))
    
    if dh is None:
        console.print("[bold red]Diffie-Hellman module not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    try:
        # Step 1: Generate DH parameters
        console.print("[yellow]🔄 Generating Diffie-Hellman parameters...[/yellow]")
        key_size = int(Prompt.ask("Key size in bits", choices=["1024", "2048", "4096"], default="2048"))
        parameters = dh.generate_parameters(generator=2, key_size=key_size, backend=default_backend())
        console.print("[bold green]✅ DH parameters generated successfully[/bold green]")
        
        # Step 2: Generate keys for Alice
        console.print("[yellow]👩 Generating keys for Alice...[/yellow]")
        private_key_alice = parameters.generate_private_key()
        public_key_alice = private_key_alice.public_key()
        console.print("[bold green]✅ Alice's keys generated successfully[/bold green]")
        
        # Step 3: Generate keys for Bob
        console.print("[yellow]👨 Generating keys for Bob...[/yellow]")
        private_key_bob = parameters.generate_private_key()
        public_key_bob = private_key_bob.public_key()
        console.print("[bold green]✅ Bob's keys generated successfully[/bold green]")
        
        # Step 4: Compute shared secrets
        console.print("[yellow]🔄 Computing shared secrets...[/yellow]")
        shared_key_alice = private_key_alice.exchange(public_key_bob)
        shared_key_bob = private_key_bob.exchange(public_key_alice)
        
        # Step 5: Derive symmetric keys
        console.print("[yellow]🔄 Deriving symmetric keys...[/yellow]")
        derived_key_alice = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key_alice)
        
        derived_key_bob = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key_bob)
        
        # Step 6: Verify keys match
        if derived_key_alice == derived_key_bob:
            console.print("[bold green]🎉 Success! The derived keys match![/bold green]")
            console.print(f"[bold green]🔑 Shared key (hex):[/bold green] {derived_key_alice.hex()}")
            
            # Option to save key
            save_key = Confirm.ask("💾 Save shared key to file?")
            if save_key:
                key_path = Prompt.ask("Key file path", default="dh_shared_key.bin")
                with open(key_path, 'wb') as f:
                    f.write(derived_key_alice)
                console.print(f"[bold green]✅ Key saved to {key_path}[/bold green]")
        else:
            console.print("[bold red]❌ ERROR: The derived keys do not match![/bold red]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error during Diffie-Hellman key exchange:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def decryption_menu():
    """Display decryption menu."""
    clear_screen()
    display_header()
    
    table = Table(title="🔓 Decryption Options")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "Classic Cipher Decryption")
    table.add_row("2", "Modern Symmetric Decryption")
    table.add_row("3", "AES Decryption")
    table.add_row("4", "RSA Decryption")
    table.add_row("0", "Back to Main Menu")
    
    console.print(table)
    
    choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4"], default="0")
    
    if choice == "1":
        handle_classic_decryption()
    elif choice == "2":
        handle_modern_symmetric_decryption()
    elif choice == "3":
        handle_aes_decryption()
    elif choice == "4":
        handle_rsa_decryption()
    
    return choice != "0"

def handle_classic_decryption():
    """Handle classic cipher decryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🏛️ Classic Cipher Decryption[/bold]", border_style="magenta"))
    
    if cesar_decrypt is None:
        console.print("[bold red]Classic cipher modules not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    # Create classic cipher decryption submenu
    table = Table(title="Classic Cipher Decryption Methods")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "César Cipher")
    table.add_row("2", "Substitution Cipher")
    table.add_row("3", "Affine Cipher")
    table.add_row("4", "Hill Cipher")
    table.add_row("5", "Playfair Cipher")
    table.add_row("6", "Vigenère Cipher")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select a cipher", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")
    
    if choice == "0":
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    if input_type == "text":
        ciphertext = Prompt.ask("Enter ciphertext")
    else:
        file_path = Prompt.ask("Enter input file path")
        ciphertext = get_file_content(file_path)
        if not ciphertext:
            return
    
    result = ""
    
    try:
        if choice == "1":  # César
            shift = int(Prompt.ask("Enter shift value (integer)", default="3"))
            result = cesar_decrypt(ciphertext, shift)
            
        elif choice == "2":  # Substitution
            alphabet = Prompt.ask("Enter substitution alphabet (26 chars)", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            result = substitution_decrypt(ciphertext, alphabet)
        elif choice == "3":  # Affine
            a = int(Prompt.ask("Enter 'a' parameter (must be coprime to 26)", default="5"))
            b = int(Prompt.ask("Enter 'b' parameter", default="8"))
            result = affine_decrypt(ciphertext, a, b)
        elif choice == "4":  # Hill
            key_matrix = Prompt.ask("Enter 2x2 key matrix (comma-separated)", default="1,2,3,4")
            # Parse the key matrix input (e.g., "1,2,3,4" for 2x2)
            matrix_values = [int(x.strip()) for x in key_matrix.split(",")]
            if len(matrix_values) == 4:
                matrix = [matrix_values[:2], matrix_values[2:]]
            elif len(matrix_values) == 9:
                matrix = [matrix_values[:3], matrix_values[3:6], matrix_values[6:]]
            else:
                console.print("[bold red]Invalid matrix size! Must be 2x2 or 3x3.[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            result = hill_decrypt(ciphertext, matrix)
        elif choice == "5":  # Playfair
            key = Prompt.ask("Enter Playfair key", default="MONARCHY")
            result = playfair_decrypt(ciphertext, key)
        elif choice == "6":  # Vigenère
            key = Prompt.ask("Enter Vigenère key", default="LEMON")
            result = vigenere_decrypt(ciphertext, key)

        # Display or save the result
        console.print(f"\n[bold green]✅ Decryption successful![/bold green]")
        if input_type == "text":
            console.print(f"[bold cyan]Ciphertext:[/bold cyan] {ciphertext}")
            console.print(f"[bold green]Decrypted text:[/bold green] {result}")
        else:
            output_path = Prompt.ask("Enter output file path", default=f"{file_path}.classic_dec")
            if save_file_content(output_path, result):
                console.print(f"[bold green]Decrypted content saved to:[/bold green] {output_path}")

    except Exception as e:
        console.print(f"[bold red]❌ Error during decryption:[/bold red] {e}")

    Prompt.ask("Press Enter to continue")

def handle_modern_symmetric_decryption():
    """Handle modern symmetric decryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔧 Modern Symmetric Decryption[/bold]", border_style="magenta"))
    
    if block_cipher_decrypt is None:
        console.print("[bold red]Modern symmetric decryption modules not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    # Create modern symmetric decryption submenu
    table = Table(title="Modern Symmetric Decryption Methods")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    table.add_column("Type", style="yellow")
    
    table.add_row("1", "Block Cipher", "Block")
    table.add_row("2", "Stream Cipher", "Stream")
    table.add_row("3", "DES", "Block (56-bit)")
    table.add_row("4", "Triple DES (3DES)", "Block (168-bit)")
    table.add_row("5", "DESX", "Block (Enhanced DES)")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select a cipher", choices=["0", "1", "2", "3", "4", "5"], default="0")
    
    if choice == "0":
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    if input_type == "text":
        ciphertext = Prompt.ask("Enter ciphertext")
    else:
        file_path = Prompt.ask("Enter input file path")
        ciphertext = get_file_content(file_path)
        if not ciphertext:
            return
    
    result = ""
    
    try:
        if choice == "1":  # Block cipher
            key = Prompt.ask("Enter Block cipher key")
            result = block_cipher_decrypt(ciphertext, key)
            
        elif choice == "2":  # Stream cipher
            key = Prompt.ask("Enter Stream cipher key")
            result = stream_cipher_decrypt(ciphertext, key)
            
        elif choice == "3":  # DES
            key = Prompt.ask("Enter DES key (8 bytes/64 bits)")
            result = des_decrypt(ciphertext, key)
            
        elif choice == "4":  # Triple DES
            console.print("[yellow]Triple DES uses three 64-bit keys[/yellow]")
            key1 = Prompt.ask("Enter first DES key")
            key2 = Prompt.ask("Enter second DES key") 
            key3 = Prompt.ask("Enter third DES key")
            result = triple_des_decrypt(ciphertext, key1, key2, key3)
            
        elif choice == "5":  # DESX
            console.print("[yellow]DESX uses DES with pre and post whitening keys[/yellow]")
            key = Prompt.ask("Enter DESX main key")
            key_pre = Prompt.ask("Enter pre-whitening key")
            key_post = Prompt.ask("Enter post-whitening key")
            result = desx_decrypt(ciphertext, key, key_pre, key_post)
        
        # Display or save the result
        console.print(f"\n[bold green]✅ Decryption successful![/bold green]")
        if input_type == "text":
            console.print(f"[bold cyan]Ciphertext:[/bold cyan] {ciphertext}")
            console.print(f"[bold green]Decrypted text:[/bold green] {result}")
        else:
            output_path = Prompt.ask("Enter output file path", default=f"{file_path}.sym_dec")
            if save_file_content(output_path, result):
                console.print(f"[bold green]Decrypted content saved to:[/bold green] {output_path}")
                
    except Exception as e:
        console.print(f"[bold red]❌ Error during decryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def handle_aes_decryption():
    """Handle AES decryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🛡️ AES Decryption[/bold]", border_style="magenta"))
    
    if aes_decrypt_block is None:
        console.print("[bold red]AES decryption module not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    
    try:
        if input_type == "text":
            ciphertext = Prompt.ask("Enter ciphertext (hex)")
            
            # Convert hex to bytes
            ciphertext_bytes = bytes.fromhex(ciphertext)
            
            key = Prompt.ask("Enter decryption key (16 bytes for AES-128)")
            
            # Make sure key is exactly 16 bytes (pad if necessary)
            if len(key.encode('utf-8')) != 16:
                key = key.ljust(16)[:16]  # Pad or truncate to 16 bytes
                console.print("[yellow]⚠️ Key adjusted to 16 bytes for AES-128[/yellow]")
            
            # Convert to bytes
            key_bytes = key.encode('utf-8')
            
            # Decrypt
            decrypted_bytes = aes_decrypt_block(ciphertext_bytes, key_bytes)
            decrypted_text = decrypted_bytes.decode('utf-8').rstrip()
            
            console.print(f"\n[bold green]✅ AES Decryption Complete![/bold green]")
            console.print(f"[bold cyan]Ciphertext:[/bold cyan] {ciphertext}")
            console.print(f"[bold green]Decrypted text:[/bold green] {decrypted_text}")
        else:
            file_path = Prompt.ask("Enter input file path")
            content = get_file_content(file_path)
            if content:
                # Process file in 16-byte blocks
                key = Prompt.ask("Enter decryption key (16 bytes for AES-128)")
                
                # Make sure key is exactly 16 bytes (pad if necessary)
                if len(key.encode('utf-8')) != 16:
                    key = key.ljust(16)[:16]  # Pad or truncate to 16 bytes
                    console.print("[yellow]⚠️ Key adjusted to 16 bytes for AES-128[/yellow]")
                
                key_bytes = key.encode('utf-8')
                
                # Convert content to bytes if it's not already
                if isinstance(content, str):
                    content_bytes = content.encode('utf-8')
                else:
                    content_bytes = content
                
                # Decrypt each block
                decrypted_bytes = b''
                for i in range(0, len(content_bytes), 16):
                    block = content_bytes[i:i+16]
                    decrypted_block = aes_decrypt_block(block, key_bytes)
                    decrypted_bytes += decrypted_block
                
                # Remove padding
                padding_length = decrypted_bytes[-1]
                decrypted_bytes = decrypted_bytes[:-padding_length]
                
                # Save to file
                output_path = Prompt.ask("Enter output file path", default=f"{file_path}.dec")
                with open(output_path, 'wb') as f:
                    f.write(decrypted_bytes)
                console.print(f"[bold green]✅ Decrypted content saved to:[/bold green] {output_path}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error during AES decryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")
def handle_rsa_signature():
    """
    Handle RSA digital signature creation and verification.
    
    Args:
        clear_screen: Function to clear the screen
        display_header: Function to display the application header
    """
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔏 RSA Digital Signature[/bold]", border_style="magenta"))

    # Create RSA signature submenu
    table = Table(title="RSA Signature Operations")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "Generate New Key Pair")
    table.add_row("2", "Sign a Message")
    table.add_row("3", "Verify a Signature")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select an operation", choices=["0", "1", "2", "3"], default="0")

    try:
        if choice == "1":
            # Generate new RSA key pair
            console.print("\n[bold]Generating RSA key pair...[/bold]")
            key_size = int(Prompt.ask("Key size in bits", choices=["1024", "2048", "3072", "4096"], default="2048"))
            
            with console.status(f"[bold green]Generating {key_size}-bit RSA keys..."):
                private_key, public_key = RSASignature.generate_keypair(key_size)
            
            console.print("[green]✓ RSA key pair generated successfully[/green]")
            
            # Display key information
            n, d = private_key
            n_pub, e = public_key
            
            console.print("\n[bold cyan]Key Information:[/bold cyan]")
            console.print(f"[cyan]Modulus n:[/cyan] ...{str(n)[-20:]}")
            console.print(f"[cyan]Public exponent e:[/cyan] {e}")
            console.print(f"[cyan]Private exponent d:[/cyan] ...{str(d)[-20:]}")
            console.print(f"[dim]Key size: {n.bit_length()} bits[/dim]")
            
            save = Prompt.ask("Do you want to save these keys?", choices=["y", "n"], default="n")
            if save == "y":
                pub_path = Prompt.ask("Public key file path", default="rsa_public.key")
                priv_path = Prompt.ask("Private key file path", default="rsa_private.key")
                
                try:
                    # Save public key (n, e)
                    with open(pub_path, 'w') as f:
                        f.write(f"{n},{e}")
                    console.print(f"[green]✓ Public key saved to {pub_path}[/green]")
                    
                    # Save private key (n, d)
                    with open(priv_path, 'w') as f:
                        f.write(f"{n},{d}")
                    console.print(f"[green]✓ Private key saved to {priv_path}[/green]")
                    
                    console.print("\n[bold yellow]⚠️  Keep your private key secure and never share it![/bold yellow]")
                except Exception as e:
                    console.print(f"[bold red]Error saving keys: {e}[/bold red]")

        elif choice == "2":
            # Sign a message
            console.print("\n[bold]Message Signing[/bold]")
            
            # Get message input
            input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
            
            if input_type == "text":
                message = Prompt.ask("Enter the message to sign")
            else:
                file_path = Prompt.ask("Enter message file path")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        message = f.read()
                    console.print(f"[green]✓ Message loaded from file ({len(message)} characters)[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error reading file: {e}[/bold red]")
                    Prompt.ask("Press Enter to continue")
                    return
            
            # Load private key
            console.print("\n[bold]Private Key[/bold]")
            priv_path = Prompt.ask("Private key file path", default="rsa_private.key")
            
            try:
                with open(priv_path, 'r') as f:
                    n, d = map(int, f.read().strip().split(','))
                
                rsa = RSASignature((n, d))
                console.print("[green]✓ Private key loaded successfully[/green]")
                console.print(f"[dim]Key size: {n.bit_length()} bits[/dim]")
            except FileNotFoundError:
                console.print(f"[bold red]Private key file not found: {priv_path}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            except Exception as e:
                console.print(f"[bold red]Error loading private key: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Sign the message
            console.print("\n[bold]Generating signature...[/bold]")
            console.print(f"[dim]Message preview: {message[:50]}{'...' if len(message) > 50 else ''}[/dim]")
            
            with console.status("[bold green]Computing RSA signature..."):
                signature = rsa.sign(message)
            
            console.print("\n[bold green]✓ Message signed successfully[/bold green]")
            console.print(f"[cyan]Signature (hex):[/cyan] {signature.hex()[:40]}...")
            console.print(f"[dim]Signature length: {len(signature)} bytes[/dim]")
            
            # Save signature
            save = Prompt.ask("\nSave signature to file?", choices=["y", "n"], default="n")
            if save == "y":
                sig_path = Prompt.ask("Signature file path", default="signature.sig")
                try:
                    with open(sig_path, 'w') as f:
                        f.write(signature.hex())
                    console.print(f"[green]✓ Signature saved to {sig_path}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error saving signature: {e}[/bold red]")

        elif choice == "3":
            # Verify a signature
            console.print("\n[bold]Signature Verification[/bold]")
            
            # Get message input
            input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
            
            if input_type == "text":
                message = Prompt.ask("Enter the original message")
            else:
                file_path = Prompt.ask("Enter message file path")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        message = f.read()
                    console.print(f"[green]✓ Message loaded from file ({len(message)} characters)[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error reading message file: {e}[/bold red]")
                    Prompt.ask("Press Enter to continue")
                    return
            
            # Load signature
            console.print("\n[bold]Signature[/bold]")
            sig_input = Prompt.ask("Load signature from", choices=["file", "manual"], default="file")
            
            try:
                if sig_input == "file":
                    sig_path = Prompt.ask("Signature file path", default="signature.sig")
                    with open(sig_path, 'r') as f:
                        signature = bytes.fromhex(f.read().strip())
                    console.print(f"[green]✓ Signature loaded from file ({len(signature)} bytes)[/green]")
                else:
                    sig_hex = Prompt.ask("Enter signature (hex)")
                    signature = bytes.fromhex(sig_hex)
                    console.print(f"[green]✓ Signature loaded ({len(signature)} bytes)[/green]")
            except Exception as e:
                console.print(f"[bold red]Error loading signature: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Load public key
            console.print("\n[bold]Public Key[/bold]")
            pub_path = Prompt.ask("Public key file path", default="rsa_public.key")
            
            try:
                with open(pub_path, 'r') as f:
                    n, e = map(int, f.read().strip().split(','))
                
                rsa = RSASignature((n, e))
                console.print("[green]✓ Public key loaded successfully[/green]")
                console.print(f"[dim]Key size: {n.bit_length()} bits[/dim]")
            except FileNotFoundError:
                console.print(f"[bold red]Public key file not found: {pub_path}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            except Exception as e:
                console.print(f"[bold red]Error loading public key: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Verify the signature
            console.print("\n[bold]Verifying signature...[/bold]")
            console.print(f"[dim]Message preview: {message[:50]}{'...' if len(message) > 50 else ''}[/dim]")
            
            with console.status("[bold green]Verifying RSA signature..."):
                is_valid = rsa.verify(message, signature)
            
            if is_valid:
                console.print("\n[bold green]✅ Signature is VALID![/bold green]")
                console.print("[green]The message has been authenticated successfully.[/green]")
                console.print("[green]The signature was created by the holder of the corresponding private key.[/green]")
            else:
                console.print("\n[bold red]❌ Signature is INVALID![/bold red]")
                console.print("[red]The message may have been tampered with, or the signature is incorrect.[/red]")
                console.print("[red]The signature verification failed.[/red]")

        elif choice == "0":
            return

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        console.print("[dim]Please check your inputs and try again.[/dim]")
        import traceback
        if console.input("[dim]Show full error details? (y/n): [/dim]").lower() == 'y':
            console.print("[dim]" + traceback.format_exc() + "[/dim]")

    Prompt.ask("\nPress Enter to continue")

def handle_rsa_decryption():
    """Handle RSA decryption."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔑 RSA Decryption[/bold]", border_style="magenta"))
    
    if generate_keys is None or decrypt_text is None:
        console.print("[bold red]RSA decryption module not available![/bold red]")
        Prompt.ask("Press Enter to continue")
        return
    
    try:
        # Load private key
        priv_path = Prompt.ask("Private key file path")
        with open(priv_path, 'r') as f:
            n, d = map(int, f.read().split(','))
            private_key = (n, d)
        
        console.print(f"[bold green]📂 Loaded private key:[/bold green] {private_key}")
        
        # Decrypt message
        input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
        
        if input_type == "text":
            ciphertext = Prompt.ask("Enter ciphertext to decrypt")
            
            # Decrypt
            decrypted = decrypt_text(ciphertext, private_key)
            console.print(f"\n[bold green]✅ RSA Decryption Complete![/bold green]")
            console.print(f"[bold cyan]Ciphertext:[/bold cyan] {ciphertext}")
            console.print(f"[bold green]Decrypted text:[/bold green] {decrypted}")
            
            # Option to save decrypted text
            save_dec = Confirm.ask("💾 Save decrypted text to file?")
            if save_dec:
                dec_path = Prompt.ask("Decrypted file path", default="decrypted.txt")
                with open(dec_path, 'w') as f:
                    f.write(decrypted)
                console.print(f"[bold green]✅ Decrypted text saved to {dec_path}[/bold green]")
        else:
            file_path = Prompt.ask("Enter input file path")
            content = get_file_content(file_path)
            if content:
                # Decrypt
                decrypted = decrypt_text(content, private_key)
                output_path = Prompt.ask("Enter output file path", default=f"{file_path}.rsa_dec")
                with open(output_path, 'w') as f:
                    f.write(decrypted)
                console.print(f"[bold green]✅ Decrypted content saved to:[/bold green] {output_path}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error during RSA decryption:[/bold red] {e}")
    
    Prompt.ask("Press Enter to continue")

def main_menu():
    """Display the main menu."""
    clear_screen()
    display_header()
    
    table = Table(title="Main Menu")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "Encryption")
    table.add_row("2", "Decryption")
    table.add_row("3", "Hashing")
    table.add_row("4", "Digital Signatures")
    table.add_row("0", "Exit")
    
    console.print(table)
    
    choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4"], default="0")
    return choice

def hashing_menu():
    """Display hashing menu and handle hashing operations."""
    clear_screen()
    display_header()
    table = Table(title="Hashing Algorithms")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Algorithm", style="green")
    table.add_row("1", "SHA-256")
    table.add_row("2", "RIPEMD-160")
    table.add_row("0", "Back")
    console.print(table)
    choice = Prompt.ask("Select an algorithm", choices=["0", "1", "2"], default="0")
    if choice == "0":
        return False

    input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
    if input_type == "text":
        data = Prompt.ask("Enter text to hash")
        data_bytes = data.encode("utf-8")
    else:
        file_path = Prompt.ask("Enter input file path")
        try:
            with open(file_path, "rb") as f:
                data_bytes = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading file:[/bold red] {e}")
            Prompt.ask("Press Enter to continue")
            return True

    try:
        if choice == "1":
            if SHA256 is None:
                console.print("[bold red]SHA-256 module not available![/bold red]")
                Prompt.ask("Press Enter to continue")
                return True
            hash_result = SHA256(data_bytes)
        elif choice == "2":
            if RIPEMD160 is None:
                console.print("[bold red]RIPEMD-160 module not available![/bold red]")
                Prompt.ask("Press Enter to continue")
                return True
            hash_result = RIPEMD160(data_bytes)
        else:
            return False

        console.print(f"\n[bold green]✅ Hashing successful![/bold green]")
        if input_type == "text":
            console.print(f"[bold cyan]Input:[/bold cyan] {data}")
        else:
            console.print(f"[bold cyan]Input file:[/bold cyan] {file_path}")
        console.print(f"[bold green]Hash:[/bold green] {hash_result}")

        if input_type == "file":
            output_path = Prompt.ask("Enter output file path", default=f"{file_path}.hash")
            try:
                with open(output_path, "w") as f:
                    f.write(str(hash_result))
                console.print(f"[bold green]Hash saved to:[/bold green] {output_path}")
            except Exception as e:
                console.print(f"[bold red]Error saving hash file:[/bold red] {e}")

    except Exception as e:
        console.print(f"[bold red]❌ Error during hashing:[/bold red] {e}")

    Prompt.ask("Press Enter to continue")
    return True

def signature_menu():
    """Display digital signature menu and handle signature operations."""
    clear_screen()
    display_header()
    table = Table(title="Digital Signature Schemes")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Scheme", style="green")
    table.add_row("1", "RSA Signature")
    table.add_row("2", "DSA")
    table.add_row("3", "ElGamal Signature")
    table.add_row("4", "Paillier Homomorphic Encryption")
    table.add_row("5", "Shamir Secret Sharing")
    table.add_row("0", "Back")
    console.print(table)
    choice = Prompt.ask("Select a scheme", choices=["0", "1", "2", "3", "4", "5"], default="0")
    if choice == "0":
        return False

    if choice == "1":
        if RSASignature is None:
            console.print("[bold red]RSA Signature module not available![/bold red]")
            console.print(result)
            console.print(realresult)
            Prompt.ask("Press Enter to continue")
            
            return True
        handle_rsa_signature()
    elif choice == "2":
        if DSA is None:
            console.print("[bold red]DSA module not available![/bold red]")
            Prompt.ask("Press Enter to continue")
            return True
        handle_dsa_signature()
    elif choice == "3":
        if ElGamalSignature is None:
            console.print("[bold red]ElGamal Signature module not available![/bold red]")
            Prompt.ask("Press Enter to continue")
            return True
        handle_elgamal_signature()
    elif choice == "4":
        if PaillierHE is None:
            console.print("[bold red]Paillier Homomorphic Encryption module not available![/bold red]")
            Prompt.ask("Press Enter to continue")
            return True
        handle_paillier_he()
    elif choice == "5":
        if ShamirSecretSharing is None:
            console.print("[bold red]Shamir Secret Sharing module not available![/bold red]")
            Prompt.ask("Press Enter to continue")
            return True
        handle_shamir_sss()
    return True





#ile
import hashlib
import random
import sympy
from typing import Tuple, Optional

# ElGamal Classes - Add these to your main file
class ElGamalParams:
    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g

class ElGamalPrivateKey:
    def __init__(self, params: ElGamalParams, x: int):
        self.params = params
        self.x = x

class ElGamalPublicKey:
    def __init__(self, params: ElGamalParams, y: int):
        self.params = params
        self.y = y

class ElGamalSignature:
    def __init__(self, key=None):
        self.key = key
    
    @staticmethod
    def generate_params(bits: int = 2048) -> ElGamalParams:
        """Generate ElGamal parameters (p, g)"""
        # Generate a large prime p
        p = sympy.nextprime(random.getrandbits(bits))
        
        # Find a generator g of the multiplicative group Z*p
        g = ElGamalSignature._find_generator(p)
        
        return ElGamalParams(p=p, g=g)
    
    @staticmethod
    def generate_keypair(params: ElGamalParams) -> Tuple[ElGamalPrivateKey, ElGamalPublicKey]:
        """Generate ElGamal key pair"""
        # Generate private key x (1 < x < p-1)
        x = random.randint(2, params.p - 2)
        
        # Calculate public key y = g^x mod p
        y = pow(params.g, x, params.p)
        
        private_key = ElGamalPrivateKey(params=params, x=x)
        public_key = ElGamalPublicKey(params=params, y=y)
        
        return private_key, public_key
    
    def sign(self, message: bytes) -> Tuple[int, int]:
        """Sign a message using ElGamal digital signature"""
        if not isinstance(self.key, ElGamalPrivateKey):
            raise ValueError("Private key required for signing")
        
        p = self.key.params.p
        g = self.key.params.g
        x = self.key.x
        
        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)
        
        while True:
            # Generate random k such that gcd(k, p-1) = 1
            k = random.randint(2, p - 2)
            if sympy.gcd(k, p - 1) == 1:
                break
        
        # Calculate r = g^k mod p
        r = pow(g, k, p)
        
        # Calculate s = k^(-1) * (h - x*r) mod (p-1)
        k_inv = sympy.mod_inverse(k, p - 1)
        s = (k_inv * (h - x * r)) % (p - 1)
        
        return (r, s)
    
    def verify(self, message: bytes, signature: Tuple[int, int]) -> bool:
        """Verify an ElGamal digital signature"""
        if not isinstance(self.key, ElGamalPublicKey):
            raise ValueError("Public key required for verification")
        
        p = self.key.params.p
        g = self.key.params.g
        y = self.key.y
        r, s = signature
        
        # Check if r and s are in valid range
        if not (0 < r < p and 0 < s < p - 1):
            return False
        
        # Hash the message
        h = int(hashlib.sha256(message).hexdigest(), 16)
        
        # Verify: g^h ≡ y^r * r^s (mod p)
        left_side = pow(g, h, p)
        right_side = (pow(y, r, p) * pow(r, s, p)) % p
        
        return left_side == right_side
    
    @staticmethod
    def _find_generator(p: int) -> int:
        """Find a generator of the multiplicative group Z*p"""
        # For simplicity, we'll use a small generator that works for most primes
        for g in range(2, min(100, p)):
            if pow(g, (p - 1) // 2, p) != 1:
                return g
        return 2  # Fallback

# Updated handle_elgamal_signature function - Replace your existing one with this
def handle_elgamal_signature():
    """Handle ElGamal digital signature creation and verification."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔏 ElGamal Digital Signature[/bold]", border_style="magenta"))

    # Create ElGamal signature submenu
    table = Table(title="ElGamal Signature Operations")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")
    
    table.add_row("1", "Generate New Key Pair")
    table.add_row("2", "Sign a Message")
    table.add_row("3", "Verify a Signature")
    table.add_row("0", "Back")
    
    console.print(table)
    
    choice = Prompt.ask("Select an operation", choices=["0", "1", "2", "3"], default="0")

    try:
        if choice == "1":
            # Generate new key pair
            console.print("\n[bold]Generating ElGamal parameters (2048 bits)...[/bold]")
            with console.status("[bold green]Generating prime numbers..."):
                params = ElGamalSignature.generate_params(bits=2048)
            console.print("[green]✓ Parameters generated[/green]")
            
            console.print("[bold]Generating key pair...[/bold]")
            private_key, public_key = ElGamalSignature.generate_keypair(params)
            console.print("[green]✓ Key pair generated[/green]")
            
            # Display public key information
            console.print("\n[bold cyan]Public Key Information:[/bold cyan]")
            console.print(f"[cyan]Modulus p:[/cyan] ...{str(params.p)[-20:]}")
            console.print(f"[cyan]Generator g:[/cyan] {params.g}")
            console.print(f"[cyan]Public value y:[/cyan] ...{str(public_key.y)[-20:]}")
            console.print(f"[dim]Full modulus bit length: {params.p.bit_length()} bits[/dim]")
            
            save = Prompt.ask("Do you want to save these keys?", choices=["y", "n"], default="n")
            if save == "y":
                pub_path = Prompt.ask("Public key file path", default="elgamal_public.key")
                priv_path = Prompt.ask("Private key file path", default="elgamal_private.key")
                try:
                    # Save public key
                    with open(pub_path, 'w') as f:
                        f.write(f"{params.p}\n{params.g}\n{public_key.y}")
                    console.print(f"[green]✓ Public key saved to {pub_path}[/green]")
                    
                    # Save private key
                    with open(priv_path, 'w') as f:
                        f.write(f"{params.p}\n{params.g}\n{private_key.x}")
                    console.print(f"[green]✓ Private key saved to {priv_path}[/green]")
                    
                    console.print("\n[bold yellow]⚠️  Keep your private key secure and never share it![/bold yellow]")
                except Exception as e:
                    console.print(f"[bold red]Error saving keys: {e}[/bold red]")

        elif choice == "2":
            # Sign a message
            console.print("\n[bold]Message to Sign[/bold]")
            input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
            
            if input_type == "text":
                message = Prompt.ask("Enter the message to sign")
                message_bytes = message.encode('utf-8')
                console.print(f"[dim]Message length: {len(message_bytes)} bytes[/dim]")
            else:
                file_path = Prompt.ask("Enter input file path")
                try:
                    with open(file_path, 'rb') as f:
                        message_bytes = f.read()
                    console.print(f"[green]✓ File loaded: {len(message_bytes)} bytes[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error reading file: {e}[/bold red]")
                    Prompt.ask("Press Enter to continue")
                    return
            
            # Load private key for signing
            console.print("\n[bold]Private Key[/bold]")
            priv_path = Prompt.ask("Enter private key file path", default="elgamal_private.key")
            try:
                with open(priv_path, 'r') as f:
                    p = int(f.readline().strip())
                    g = int(f.readline().strip())
                    x = int(f.readline().strip())
                params = ElGamalParams(p=p, g=g)
                private_key = ElGamalPrivateKey(params=params, x=x)
                
                # Create ElGamal signature object with private key
                signer = ElGamalSignature(private_key)
                console.print("[green]✓ Private key loaded successfully[/green]")
            except FileNotFoundError:
                console.print(f"[bold red]Private key file not found: {priv_path}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            except Exception as e:
                console.print(f"[bold red]Error loading private key: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Sign the message
            console.print("\n[bold]Generating signature...[/bold]")
            with console.status("[bold green]Computing signature..."):
                signature = signer.sign(message_bytes)
            
            console.print("\n[bold green]✓ Signature generated successfully[/bold green]")
            console.print(f"[cyan]Signature r:[/cyan] ...{str(signature[0])[-20:]}")
            console.print(f"[cyan]Signature s:[/cyan] ...{str(signature[1])[-20:]}")
            console.print(f"[dim]Full signature lengths: r={signature[0].bit_length()} bits, s={signature[1].bit_length()} bits[/dim]")
            
            # Save signature if requested
            save = Prompt.ask("\nDo you want to save the signature?", choices=["y", "n"], default="n")
            if save == "y":
                output_path = Prompt.ask("Enter output file path", default="signature.txt")
                try:
                    with open(output_path, 'w') as f:
                        f.write(f"{signature[0]}\n{signature[1]}")
                    console.print(f"[green]✓ Signature saved to {output_path}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error saving signature: {e}[/bold red]")

        elif choice == "3":
            # Verify a signature
            console.print("\n[bold]Message Verification[/bold]")
            input_type = Prompt.ask("Input type", choices=["text", "file"], default="text")
            
            if input_type == "text":
                message = Prompt.ask("Enter the original message")
                message_bytes = message.encode('utf-8')
                console.print(f"[dim]Message length: {len(message_bytes)} bytes[/dim]")
            else:
                file_path = Prompt.ask("Enter message file path")
                try:
                    with open(file_path, 'rb') as f:
                        message_bytes = f.read()
                    console.print(f"[green]✓ File loaded: {len(message_bytes)} bytes[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error reading message file: {e}[/bold red]")
                    Prompt.ask("Press Enter to continue")
                    return
            
            # Get signature components
            console.print("\n[bold]Signature Components[/bold]")
            sig_input = Prompt.ask("Load signature from", choices=["file", "manual"], default="file")
            
            try:
                if sig_input == "file":
                    sig_path = Prompt.ask("Enter signature file path", default="signature.txt")
                    with open(sig_path, 'r') as f:
                        r = int(f.readline().strip())
                        s = int(f.readline().strip())
                    console.print("[green]✓ Signature loaded from file[/green]")
                else:
                    r = int(Prompt.ask("Enter signature component r"))
                    s = int(Prompt.ask("Enter signature component s"))
                
                console.print(f"[dim]Signature lengths: r={r.bit_length()} bits, s={s.bit_length()} bits[/dim]")
            except (ValueError, FileNotFoundError) as e:
                console.print(f"[bold red]Error loading signature: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Load public key for verification
            console.print("\n[bold]Public Key[/bold]")
            pub_path = Prompt.ask("Enter public key file path", default="elgamal_public.key")
            try:
                with open(pub_path, 'r') as f:
                    p = int(f.readline().strip())
                    g = int(f.readline().strip())
                    y = int(f.readline().strip())
                params = ElGamalParams(p=p, g=g)
                public_key = ElGamalPublicKey(params=params, y=y)
                
                # Create ElGamal signature object with public key
                verifier = ElGamalSignature(public_key)
                console.print("[green]✓ Public key loaded successfully[/green]")
            except FileNotFoundError:
                console.print(f"[bold red]Public key file not found: {pub_path}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            except Exception as e:
                console.print(f"[bold red]Error loading public key: {e}[/bold red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Verify the signature
            console.print("\n[bold]Verifying signature...[/bold]")
            with console.status("[bold green]Computing verification..."):
                is_valid = verifier.verify(message_bytes, (r, s))
            
            if is_valid:
                console.print("\n[bold green]✅ Signature is VALID![/bold green]")
                console.print("[green]The message has been authenticated successfully.[/green]")
            else:
                console.print("\n[bold red]❌ Signature is INVALID![/bold red]")
                console.print("[red]The message may have been tampered with or the signature is incorrect.[/red]")

        elif choice == "0":
            return

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        console.print("[dim]Please check your inputs and try again.[/dim]")
        import traceback
        if console.input("[dim]Show full error details? (y/n): [/dim]").lower() == 'y':
            console.print("[dim]" + traceback.format_exc() + "[/dim]")

    Prompt.ask("\nPress Enter to continue")


def handle_paillier_he():
    """Handle Paillier Homomorphic Encryption operations."""
    clear_screen()
    display_header()
    console.print(Panel("[bold]🔐 Paillier Homomorphic Encryption[/bold]", border_style="magenta"))
    
    try:
        # Generate new keypair
        console.print("[yellow]Generating new keypair (this may take a moment)...[/yellow]")
        phe = PaillierHE()
        public_key, private_key = phe.generate_keypair(bits=1024)
        phe.public_key = public_key
        phe.private_key = private_key
        console.print("[bold green]✅ Keypair generated successfully![/bold green]")

        while True:
            operation = Prompt.ask(
                "\nChoose operation",
                choices=["1", "2", "3", "0"],
                default="1"
            )
            
            if operation == "0":
                break
                
            if operation == "1":  # Encrypt/Decrypt test
                m = int(Prompt.ask("Enter a number to encrypt", default="42"))
                console.print("\n[yellow]Encrypting value...[/yellow]")
                c = phe.encrypt(m)
                console.print("[bold green]✅ Value encrypted![/bold green]")
                console.print(f"[cyan]Original number:[/cyan] {m}")
                console.print(f"[cyan]Encrypted value:[/cyan] {c}")
                
                decrypted = phe.decrypt(c)
                console.print("\n[yellow]Decrypting value...[/yellow]")
                console.print(f"[bold green]Decrypted value:[/bold green] {decrypted}")
                console.print(f"[yellow]Verification: Original = {m}, Decrypted = {decrypted}[/yellow]")
                
            elif operation == "2":  # Homomorphic addition
                m1 = int(Prompt.ask("Enter first number", default="30"))
                m2 = int(Prompt.ask("Enter second number", default="12"))
                
                console.print("\n[yellow]Encrypting values...[/yellow]")
                c1 = phe.encrypt(m1)
                c2 = phe.encrypt(m2)
                console.print("[bold green]✅ Values encrypted![/bold green]")
                
                console.print("\n[yellow]Performing homomorphic addition...[/yellow]")
                c_sum = PaillierHE.add_encrypted(c1, c2, public_key)
                decrypted_sum = phe.decrypt(c_sum)
                
                console.print(f"\n[bold green]Results:[/bold green]")
                console.print(f"[cyan]First number:[/cyan] {m1}")
                console.print(f"[cyan]Second number:[/cyan] {m2}")
                console.print(f"[bold green]Homomorphic sum:[/bold green] {decrypted_sum}")
                console.print(f"[yellow]Verification: {m1} + {m2} = {decrypted_sum}[/yellow]")
                
            elif operation == "3":  # Homomorphic multiplication by constant
                m = int(Prompt.ask("Enter base number", default="15"))
                k = int(Prompt.ask("Enter constant multiplier", default="5"))
                
                console.print("\n[yellow]Encrypting value...[/yellow]")
                c = phe.encrypt(m)
                console.print("[bold green]✅ Value encrypted![/bold green]")
                
                console.print(f"\n[yellow]Performing homomorphic multiplication by {k}...[/yellow]")
                c_mult = PaillierHE.multiply_constant(c, k, public_key)
                decrypted_mult = phe.decrypt(c_mult)
                
                console.print(f"\n[bold green]Results:[/bold green]")
                console.print(f"[cyan]Base number:[/cyan] {m}")
                console.print(f"[cyan]Multiplier:[/cyan] {k}")
                console.print(f"[bold green]Homomorphic product:[/bold green] {decrypted_mult}")
                console.print(f"[yellow]Verification: {m} * {k} = {decrypted_mult}[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error in Paillier operations:[/bold red] {e}")
        import traceback
        traceback.print_exc()

    Prompt.ask("\nPress Enter to return to menu")

def handle_shamir_sss():
    """Handle Shamir Secret Sharing operations."""
    console.print(Panel("[bold]🔏 Shamir Secret Sharing[/bold]", border_style="magenta"))
    # Placeholder for Shamir SSS logic
    console.print("[yellow]Shamir SSS functionality not implemented in this template.[/yellow]")
    Prompt.ask("Press Enter to continue")

def main():
    """Main application entry point."""
    while True:
        choice = main_menu()
        if choice == "0":
            console.print("[bold blue]Thank you for using the Cryptography Toolkit![/bold blue]")
            break
        elif choice == "1":
            while encryption_menu():
                pass
        elif choice == "2":
            while decryption_menu():
                pass
        elif choice == "3":
            while hashing_menu():
                pass
        elif choice == "4":
            while signature_menu():
                pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user[/bold red]")
        sys.exit(0)
