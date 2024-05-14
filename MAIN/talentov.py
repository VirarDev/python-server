from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64
import importlib
import sys



app = FastAPI()

# Allowing CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = b"JAY23_Vt-GcUJ0JKNUglyO7gCuK_87MK"
valid_keys = ['JY6odVt-GcUJ0JKNUglyO7gCuKO_4T1FZR8rIKznZpg']

# Function to encrypt data using AES
def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')

# Function to decrypt data using AES
def decrypt_aes(encrypted_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
        decrypted_data = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
        return True,decrypted_data.decode('utf-8')
    except UnicodeDecodeError:
        return False,None

# Function to check authentication
def authenticate(request: Request):
    encrypted_key = request.headers.get('X-Encrypted-Key')

    if not encrypted_key:
        raise HTTPException(status_code=401, detail="Unauthorized: X-Encrypted-Key header is missing")

    can_decrypt,decrypted_key = decrypt_aes(encrypted_key, SECRET_KEY)

    if(can_decrypt == False):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid key")

    if decrypted_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid key")

sys.SharedMemory = {}
sys.SharedMemory["Modules"] = {}

# Function to call function from the given module path
def call_function_from_path(module_path, function, method, data):
    try:
        if(module_path in sys.SharedMemory["Modules"]):
            module = sys.SharedMemory["Modules"][module_path]
            # print("Using existing module")
        else:
            module = importlib.import_module(f'functions.{module_path}')
            sys.SharedMemory["Modules"][module_path] = module
            # print("importing module")

        function_obj = getattr(module, function, None)
        if function_obj is not None and callable(function_obj):
            if method == 'GET':
                return function_obj()
            elif method == 'POST':
                return function_obj(data)
            else:
                raise HTTPException(status_code=400, detail="Invalid method")
        else:
            raise HTTPException(status_code=404)
    except (ImportError, AttributeError) as e:
        return (str(e)+" - At call_function_from_path")

@app.get("/")
@app.post("/")
def version():
    return "Hello World! from jay and hari version - 25 November 2023 12:40 AM"

@app.get("/{path:path}")
@app.post("/{path:path}")
async def dynamic_route(path: str, request: Request):
    authenticate(request)

    
    parts = path.split('/')

    if len(parts) < 2:
        raise HTTPException(status_code=404)

    package = '.'.join(parts[:-1])
    function = parts[-1]

    method = request.method
    # data = request.json() if method == 'POST' else None
    data = await request.json() if method == 'POST' else None

    result = call_function_from_path(package, function, method, data)

    return Response(content=result, media_type="application/json")


def run(app,port):
    import sys
    is_live = "ubuntu" in sys.argv[0]
    if is_live:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port, ssl_keyfile="MAIN/privkey.pem", ssl_certfile="MAIN/fullchain.pem")
    else:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port)

sys.PORT_NUMBER = 5000
if __name__ == "__main__":
    run("talentov",sys.PORT_NUMBER)