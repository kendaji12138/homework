from pyasn1.codec.der.decoder import decode as der_decoder
from person import Person

if __name__ == "__main__":
    text = file = open('test_per', 'rb').read()
    result = der_decoder(text, asn1Spec=Person())
    print(result[0].prettyPrint())
