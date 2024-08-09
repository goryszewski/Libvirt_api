import base64
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime


def sign_certificate_request(csr_string, days=10):
    pre_decode_csr = base64.urlsafe_b64decode(csr_string + "==")

    csr = x509.load_der_x509_csr(pre_decode_csr, default_backend())

    with open(".secrets/Kubernetes_CA.key", "rb") as key_file:
        ca_private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    with open(".secrets/Kubernetes_CA.pem", "rb") as cert_file:
        ca_cert = x509.load_pem_x509_certificate(cert_file.read(), default_backend())

    serial_number = x509.random_serial_number()

    san_extension = None
    try:
        san_extension = csr.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
    except x509.ExtensionNotFound:
        san_extension = None

    cert_builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(serial_number)
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
    )
    if san_extension:
        cert_builder = cert_builder.add_extension(
            san_extension.value,
            critical=False,
        )

    cert = cert_builder.sign(ca_private_key, hashes.SHA256(), default_backend())

    with open(".secrets/newcer", "wb") as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

    return cert.public_bytes(serialization.Encoding.PEM)
