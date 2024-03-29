import json
import sha3 

def sortCharacters(data):
    l = list(json.dumps(data))
    l.sort()

    return "".join(l)

def keccakHash(data):
    hash = sha3.keccak_256()
    hash.update(sortCharacters(data).encode('utf-8'))

    return hash.hexdigest()