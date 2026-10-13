# PE 89.1 · Fundamentos de ChaCha20

Actividad resuelta en Python con PyCryptodome. El archivo [`chacha20_ejercicio.py`](chacha20_ejercicio.py) cifra el mensaje de la parte 1, descifra la parte 2 y recupera el texto disponible del extra mediante `seek(8)`.

## Instalación y ejecución

Con Python 3 instalado, abre esta carpeta en Visual Studio Code y ejecuta en la terminal de PowerShell:

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe .\chacha20_ejercicio.py
```

Si `python` no está disponible, utiliza `py -m venv .venv` o instala Python. Después de crear `.venv`, también puedes ejecutar el programa con **Ctrl + Mayús + B** y la tarea **Ejecutar ejercicio ChaCha20**. No hace falta activar el entorno: se invoca directamente su intérprete.

## Parte 1: cifrado

El texto se codifica en UTF-8 porque el cifrador trabaja con bytes. Con la clave y el nonce del enunciado, el texto cifrado en hexadecimal es:

```text
4568713083cb8f6fabedd05306ccbbec77e9ec281fc545db88186057c379516ead33ec2e08929f92b8778a0d
```

La salida del programa también muestra el resultado como literal `bytes`. Las dos representaciones contienen exactamente los mismos bytes; hexadecimal suele ser más cómodo para copiar sin confundir caracteres de escape.

La clave tiene **32 bytes = 256 bits**. El nonce utilizado tiene **8 bytes = 64 bits**.

PyCryptodome admite un nonce de **8 o 12 bytes** con ChaCha20. Con **24 bytes** utiliza XChaCha20. **16 bytes no se admiten**. Un nonce más largo amplía el espacio de valores posibles y hace menos probable una repetición accidental cuando se generan nonces al azar. Sin embargo, no sustituye la obligación de que cada nonce sea único para una misma clave. En la variante de 12 bytes, el contador ocupa 32 bits y cada mensaje tiene un límite aproximado de 256 GiB (unos 275 GB); en la variante original de 8 bytes, el contador ocupa 64 bits. Los 24 bytes corresponden a XChaCha20, que facilita el uso de nonces aleatorios en grandes cantidades.

Si se reutilizan **clave y nonce**, se genera el mismo flujo de clave desde el inicio. Puesto que `C1 = P1 XOR K` y `C2 = P2 XOR K`, entonces `C1 XOR C2 = P1 XOR P2`. Eso filtra la relación entre los textos originales y puede permitir recuperar contenido. El nonce no necesita mantenerse secreto; sí debe evitarse repetirlo con la misma clave. Los parámetros fijos de esta actividad se usan solo para reproducir el ejercicio.

ChaCha20 proporciona **confidencialidad**, pero no verifica si el cifrado fue alterado. ChaCha20-Poly1305 añade una etiqueta de autenticación que permite verificar **integridad y autenticidad** antes de aceptar el mensaje. En una aplicación real conviene usar esta modalidad autenticada y un nonce nuevo por mensaje.

## Parte 2: descifrado

Con el texto cifrado proporcionado, la misma clave y el mismo nonce, se obtiene:

```text
Este es un mensaje secreto que quiero que descifres
```

El programa crea un cifrador nuevo para empezar desde la posición inicial del keystream y convierte los bytes descifrados de UTF-8 a texto.

## Extra: sincronización del keystream

`seek(8)` coloca el cifrador en el noveno byte del keystream, porque la posición inicial es cero. Así, el primer byte cifrado que sí llegó se combina con el noveno byte del flujo. El texto recuperado es:

```text
saje ha sufrido un error en la transmision
```

Los primeros 8 bytes del texto cifrado no llegaron, por lo que **no se pueden recuperar sus correspondientes 8 bytes de texto plano** con este fragmento. `seek()` permite descifrar el resto; no reconstruye lo perdido. Para mensajes reales también habría que comprobar su autenticidad.

## Preguntas del ejercicio y respuestas

1. **¿Cuál es el texto cifrado resultante?** En hexadecimal: `4568713083cb8f6fabedd05306ccbbec77e9ec281fc545db88186057c379516ead33ec2e08929f92b8778a0d`. El programa también lo imprime como `bytes`.
2. **¿Qué tamaño tiene el nonce utilizado?** 8 bytes, equivalentes a 64 bits. La clave mide 32 bytes, equivalentes a 256 bits.
3. **¿Se puede usar un nonce de 12 o 16 bytes?** Sí, 12 bytes con ChaCha20 en PyCryptodome; 16 bytes no. Un nonce de 24 bytes selecciona XChaCha20.
4. **¿Qué implica usar un nonce mayor?** Aumenta el espacio de posibles nonces y reduce las colisiones accidentales cuando se eligen al azar. Cambia la variante y el espacio disponible para el contador: con 12 bytes, el límite por mensaje es aproximadamente 256 GiB. La unicidad del nonce sigue siendo obligatoria.
5. **¿Qué pasa si se reutilizan clave y nonce?** Se repite el keystream. Un atacante que tenga ambos cifrados puede calcular `C1 XOR C2 = P1 XOR P2`, lo que filtra información sobre los mensajes y, si conoce uno, permite recuperar la parte correspondiente del otro.
6. **¿Qué diferencia hay entre ChaCha20 y ChaCha20-Poly1305?** ChaCha20 cifra y proporciona confidencialidad. ChaCha20-Poly1305 además produce una etiqueta que el receptor verifica para detectar alteraciones y autenticar el mensaje. Ambos necesitan un nonce único por clave.
7. **¿Cuál es el texto plano de la parte 2?** «Este es un mensaje secreto que quiero que descifres».
8. **Extra: ¿cómo se sincroniza el keystream y qué se recupera?** Se crea un cifrador nuevo con la misma clave y el mismo nonce, se llama a `seek(8)` y después a `decrypt()`. Se obtiene «saje ha sufrido un error en la transmision». Los ocho bytes anteriores no se pueden recuperar a partir del fragmento recibido.

## Qué hace cada parte del programa

- `ChaCha20.new(key=CLAVE, nonce=NONCE)` crea un cifrador nuevo. Cifrar y descifrar empiezan desde la posición cero con objetos distintos.
- `encode("utf-8")` convierte texto en bytes; `decode("utf-8")` hace la conversión inversa.
- `encrypt()` y `decrypt()` combinan datos y keystream mediante XOR. Con los mismos parámetros y la misma posición, esa operación es reversible.
- `seek(desplazamiento)` mueve la posición absoluta del flujo en bytes. En el extra, el desplazamiento es 8.

## Archivos del proyecto

- `chacha20_ejercicio.py`: implementación de las dos partes y el extra.
- `requirements.txt`: dependencia PyCryptodome.
- `.vscode/`: configuración opcional para ejecutar el programa desde Visual Studio Code.

## Fuentes

- [PyCryptodome: ChaCha20 y XChaCha20](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20.html)
- [PyCryptodome: ChaCha20-Poly1305](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20_poly1305.html)
