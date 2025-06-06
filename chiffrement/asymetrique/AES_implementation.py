from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

# AES S-box
Sbox = [
    # 0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# AddRoundKey
def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

# SubBytes
def sub_bytes(state):
    return [Sbox[b] for b in state]

# ShiftRows
def shift_rows(state):
    return [
        state[0], state[5], state[10], state[15],
        state[4], state[9], state[14], state[3],
        state[8], state[13], state[2], state[7],
        state[12], state[1], state[6], state[11]
    ]

# Simplified AES round for demo
def aes_encrypt_block(block, key):
    state = list(block)
    state = add_round_key(state, key)
    for _ in range(9):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, key)  # In real AES, use round keys
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key)
    return bytes(state)

# 16-byte plaintext and key (must be exactly 16 bytes for AES-128)
plaintext = b"example16bytes!!"
key = b"mysecretkey12345"

# Encrypt one block
ciphertext = aes_encrypt_block(plaintext, key)
print("Ciphertext:", ciphertext.hex())

# AES inverse S-box
InvSbox = [0] * 256
for i, s in enumerate(Sbox):
    InvSbox[s] = i

def inv_sub_bytes(state):
    return [InvSbox[b] for b in state]

def inv_shift_rows(state):
    return [
        state[0], state[13], state[10], state[7],
        state[4], state[1],  state[14], state[11],
        state[8], state[5],  state[2],  state[15],
        state[12], state[9], state[6],  state[3]
    ]

def aes_decrypt_block(block, key):
    state = list(block)
    state = add_round_key(state, key)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    for _ in range(9):
        state = add_round_key(state, key)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
    state = add_round_key(state, key)
    return bytes(state)

# Example use
decrypted = aes_decrypt_block(ciphertext, key)
print("Decrypted:", decrypted)

console = Console()

def aes_menu():
    while True:
        console.clear()
        console.print(Panel("[bold cyan]AES Demo Menu[/bold cyan]", border_style="magenta"))
        table = Table(title="AES Operations")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_row("1", "Encrypt a 16-byte block")
        table.add_row("2", "Decrypt a 16-byte block")
        table.add_row("0", "Exit")
        console.print(table)
        choice = Prompt.ask("Select an option", choices=["0", "1", "2"], default="0")
        if choice == "0":
            console.print("[bold blue]Exiting AES menu.[/bold blue]")
            break
        elif choice == "1":
            plaintext = Prompt.ask("Enter 16-byte plaintext (ASCII)", default="example16bytes!!")
            key = Prompt.ask("Enter 16-byte key (ASCII)", default="mysecretkey12345")
            if len(plaintext) != 16 or len(key) != 16:
                console.print("[bold red]Both plaintext and key must be exactly 16 bytes![/bold red]")
                Prompt.ask("Press Enter to continue")
                continue
            ciphertext = aes_encrypt_block(plaintext.encode(), key.encode())
            console.print(f"[bold green]Ciphertext (hex):[/bold green] {ciphertext.hex()}")
            Prompt.ask("Press Enter to continue")
        elif choice == "2":
            ciphertext_hex = Prompt.ask("Enter ciphertext (hex)")
            key = Prompt.ask("Enter 16-byte key (ASCII)", default="mysecretkey12345")
            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                if len(ciphertext) != 16 or len(key) != 16:
                    raise ValueError
            except Exception:
                console.print("[bold red]Invalid ciphertext or key length![/bold red]")
                Prompt.ask("Press Enter to continue")
                continue
            decrypted = aes_decrypt_block(ciphertext, key.encode())
            try:
                decrypted_text = decrypted.decode()
            except Exception:
                decrypted_text = str(decrypted)
            console.print(f"[bold green]Decrypted text:[/bold green] {decrypted_text}")
            Prompt.ask("Press Enter to continue")

if __name__ == "__main__":
    aes_menu()
