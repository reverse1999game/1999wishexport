import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import ExtendedKeyUsageOID, NameOID

KEY_SIZE = 2048
CA_EXPIRY = datetime.timedelta(days=10 * 365)

ORGANIZATION = "anything"
CN = "anything"

def create_ca():
    now = datetime.datetime.now()

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
    )
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, CN),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION)
    ])
    builder = x509.CertificateBuilder()
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.subject_name(name)
    builder = builder.not_valid_before(now - datetime.timedelta(days=2))
    builder = builder.not_valid_after(now + CA_EXPIRY)
    builder = builder.issuer_name(name)
    builder = builder.public_key(private_key.public_key())
    builder = builder.add_extension(x509.BasicConstraints(
        ca=True, path_length=None), critical=True)
    builder = builder.add_extension(x509.ExtendedKeyUsage(
        [ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
    builder = builder.add_extension(
        x509.KeyUsage(
            digital_signature=False,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False,
        ), critical=True)
    builder = builder.add_extension(x509.SubjectKeyIdentifier.from_public_key(
        private_key.public_key()), critical=False)
    cert = builder.sign(private_key=private_key,
                        algorithm=hashes.SHA256())
    return private_key, cert


def creatCA():
    key, ca = create_ca() # to run the function above
    key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    ca = ca.public_bytes(serialization.Encoding.PEM)

    pem_content = key+ca

    with open("mitmproxy-ca.pem", "wb") as w:
        w.write(pem_content)
