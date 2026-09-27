import hashlib
import os

class PythonPureWrapper:
    """Encriptador temporal compatible con Python 3.14 en desarrollo"""
    def hash(self, password: str) -> str:
        # Generamos una sal segura de forma nativa
        salt = os.urandom(16).hex()
        # Creamos el hash usando SHA-256 (nativo de Python, nunca falla)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
        
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        try:
            salt, hashed = hashed_password.split("$")
            check_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return check_hash == hashed
        except Exception:
            return False

# Declaramos los mapeos exactos que consumen tus archivos de rutas y servicios
pwd_context = PythonPureWrapper()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
