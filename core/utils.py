import os
import hashlib

# Block size to read file (for hash SHA256).
BLOCK_SIZE = 65535

def generate_sha256(filepath):
    if not os.path.isfile(filepath):
        raise Exception("File '{0}' does not exist.".format(filepath))
    sha256_hash = hashlib.sha256()
    with open(filepath,"rb") as f:
        # Read and update hash string value in blocks
        for byte_block in iter(lambda: f.read(BLOCK_SIZE), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()