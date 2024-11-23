from cryptography.fernet import Fernet
import urllib.parse
import base64

# Generate a key and instantiate a Fernet instance (only do this once)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_url_params(params):
    query_string = urllib.parse.urlencode(params)
    encrypted_query = cipher_suite.encrypt(query_string.encode()).decode()
    return encrypted_query

def encrypt_url_param(param): 
    encrypted_text = cipher_suite.encrypt(param.encode()) 
    encrypted_text_base64 = base64.urlsafe_b64encode(encrypted_text).decode('utf-8') 
    return encrypted_text_base64



# To decrypt the parameters
def decrypt_url_params(encrypted_query):
    decrypted_query = cipher_suite.decrypt(urllib.parse.unquote_plus(encrypted_query).encode()).decode()
    params = urllib.parse.parse_qs(decrypted_query)
    return params

if __name__ == "__main__":
    params = {"param1": "value1", "param2": "value2"}
    url = encrypt_url_params(params)
    print(url)
else:
    print(__name__)