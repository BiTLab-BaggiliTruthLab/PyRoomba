from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

data = {
    "edek_list": "EjKpu1durwY0bjySx4ynhV2fjZYsYU3kHaKML0SiuYsJW5Ai+WIaTdaqCRk8gjnqhfqNWGOeBnF6siXX950654z3nHOSg+Ma9IhpdsLbhLLPU465pLsqhBtsHagrg2SHGVyS5z2efHvc973AzPqzCxP1A+z0htLZRvJISqGtyqwDloHscJfbJAlmzS5zcjBNV4Lia3UjAjNMXoMNvVBWPxBT89R477FUxseCYTI4lAHzaOFUyjhtrvvxoob6Vq59yuda0AhTjF2omipCkLs86VF9n4HbHgAaLT7kmQwaxOrr6YMEtBZYQUjmRwuiKZIb1OQf/ZRxxk65lesZIGc6/xyesIvs4Fm3SsYrqYUtRkPIBjPWGLtlnWvds/0l1OxfGhx5T508zOqVuFmUQss10ebjmSFJHy1XzDxVj08co+Y8G13MGcOTigIJM5/OyKLw81EthnW9T4U6nruMAj3DY/yqKp0k/eXdEG5lFcqOxtwM3mV79vAEM8PkqnuVbtBKPcsTfkVj0LauAsu9WkVQs/5S12VsDQzh0Nun38Q/XLDbvADzmB4kvG8PYrQIFJ85izC6fah2KdD8FiTI+P7XKtk5qJOk4mtO3q+ZXTlzyuO3ik4e0TWLQ02clgV4NPyJ22sdGpBwtu96F4Cjj+Ln2k7zkWWIf1D8cr79cONXKhU8wPZCoTxstC1aHrBhBQgX5bYSBg8vos6KX/C/ILIeT6ZMuUUpRjoZ0rB+jScNc0bNYwFraj3TEIC8Q6suZLAEwzaf5oISsFOhaZyZyxynzbPWEfYjDIz8ujHsFCnldpwh3q+YgmK7M1rQFQyZdfz2NQc1x0+WREaqXRzcrdm+i1vXuYnNUb35N24xrIumvEOD8yQim1JEksuzUNJ0aY3GDHsfsBHOfrMGIR133BdRB4yA5+DBNpB8Jse7e0ja40OjY395ZcWN1JbONYOqyogG+etOEGkduCERyvA6FKPEzb8I7HaerI7VhOR7ZteEbN8tYDOWK6CPt9YE5euw2UHqx8pMI7QzJPDrsRJ1mxY+D+Hri+N6CK5wW4EkvadNMt8g9vSfdUCHKBboYyyWkpHQcStIE4C110j+fQW4E+8mexIFaWI/PvxENmqZ6aZTzYJgLocWX2TCkuUfIwBfuoHw==",  # truncated for brevity
    "edek_list_hash": "sImuC/fsQF9QkNqOTU35giiAExZNXEaZsPPIQI9G23k=",
    "edek_list_iv": "xZmHA4bcOjo+L4RIAyA5Xg=="
}

# Extract the encrypted key and its IV from the provided data
enc_key = b64decode(data["edek_list"])
iv = b64decode("ANDROID-7788897D-62F5-4399-B5DE-BD1E43A00EE9")

# Assuming for the sake of this example that the base64-decoded edek_list is the symmetric key.
# In real-world scenario, this EDEK should be decrypted with a master key.
key = enc_key

# Decrypt the encrypted JPEG file
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()

with open('17c32780-10ed-4a1a-8744-ada6b81fdafa.jpg.enc', 'rb') as f_enc, \
        open('17c32780-10ed-4a1a-8744-ada6b81fdafa.jpg', 'wb') as f_dec:
    f_dec.write(decryptor.update(f_enc.read()) + decryptor.finalize())
