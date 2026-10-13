"""Actividad PE 89.1: cifrado, descifrado y sincronización con ChaCha20.

Los parámetros fijos proceden del enunciado. Su reutilización aquí sirve solo
para reproducir el ejercicio; en una aplicación real sería insegura.
"""

from Crypto.Cipher import ChaCha20


CLAVE = b'z\xe8~"\xcayW\x14g\x18+\x1c+\xf9\x80\x06P\x9ej\x888\xb4G\xdf\xe4\xc50,\x8dY\x80\x19'
NONCE = b'\xd6\x7f6\xc7\xe8i*\xa4'
MENSAJE = "Este es un mensaje secreto que quiero cifrar"

CIFRADO_PARTE_2 = (
    b'Ehq0\x83\xcb\x8fo\xab\xed\xd0S\x06\xcc\xbb\xecw\xe9\xec(\x1f\xc5E\xdb'
    b'\x88\x18`W\xc3yQn\xad3\xec.\x08\x92\x8d\x8e\xbb%\x8f\x1a\xa6\xc9=\x15\x0f5\xaa'
)

CIFRADO_SIN_8_BYTES = (
    b"\xad\xe2\x9a[C\xca\xa9\xadn\xf9\xaa)\x13\xc2X\x9e\x89\x19`C\xc4n\x1em"
    b"\xf8?\xe7|\x0b\xd3\xdc\x8f\xacd\x85\x0c\xb8\xc3'\x1a\x12>"
)


def cifrar(texto: str) -> bytes:
    """Convierte texto UTF-8 a bytes y lo cifra desde la posición cero."""
    cifrador = ChaCha20.new(key=CLAVE, nonce=NONCE)
    return cifrador.encrypt(texto.encode("utf-8"))


def descifrar(datos: bytes, desplazamiento: int = 0) -> str:
    """Descifra desde una posición en bytes y convierte el resultado a texto."""
    cifrador = ChaCha20.new(key=CLAVE, nonce=NONCE)
    cifrador.seek(desplazamiento)
    return cifrador.decrypt(datos).decode("utf-8")


def main() -> None:
    assert len(CLAVE) == 32
    assert len(NONCE) == 8

    cifrado = cifrar(MENSAJE)
    print("PARTE 1")
    print("Texto plano:", MENSAJE)
    print("Texto cifrado (bytes):", repr(cifrado))
    print("Texto cifrado (hex):", cifrado.hex())
    print("Tamaño del nonce:", len(NONCE), "bytes")

    print("\nPARTE 2")
    print("Texto plano resultante:", descifrar(CIFRADO_PARTE_2))

    print("\nEXTRA")
    print("Texto recuperado tras perder 8 bytes:", descifrar(CIFRADO_SIN_8_BYTES, 8))


if __name__ == "__main__":
    main()
