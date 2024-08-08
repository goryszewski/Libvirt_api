from flask_restful import Resource
from flask import request, jsonify, Response, make_response
import base64, json
from lib.logging import logging
from datetime import datetime, timedelta

from Model.AcmeAccount import AccountModel, AccountSchema

url = "http://10.17.3.1:8050/acme"


def decode_base64_fix(data):
    fix = "=" * int(len(data) % 4)
    payload = base64.b64decode(data + fix)
    return payload.decode()


class Directory(Resource):
    def __init__(self):
        pass

    def get(self):
        output = {
            "newNonce": f"{url}/new-nonce",
            "newAccount": f"{url}/new-account",
            "newOrder": f"{url}/new-order",
            "revokeCert": f"{url}/revoke-cert",
            "keyChange": f"{url}/key-change",
        }
        return output, 200

    def post(sefl):
        return "", 501

    def put(self):
        return "", 501


class NewAccount(Resource):
    def __init__(self):
        self.account_schema = AccountSchema()

    def get(self):
        return "", 501

    def post(self):
        request_json = request.get_json()
        headers = dict(request.headers)
        # protected = decode_base64_fix(request_json["protected"])
        # logging.info(headers)

        payload = json.loads(decode_base64_fix(request_json["payload"]))

        error = self.account_schema.validate(payload)
        if error:
            logging.error(error)
            return error, 422

        account = AccountModel.objects(**payload).first()

        rc = 501
        if account:
            rc = 200
        else:
            rc = 201
            account = AccountModel(**self.account_schema.dump(payload))
            account.save()

        output = {
            "contact": account.contact,
            "status": "valid",
            "orders": f"{url}/account/{account.id}/orders",
        }

        response = make_response(jsonify(output), rc)
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response

    def put(self):
        return "", 501


class AuthZ(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl, id):
        request_json = request.get_json()
        # logging.info(f"id - {id}")
        protected = decode_base64_fix(request_json["protected"])
        # logging.info(f"protected - {protected}")

        payload = decode_base64_fix(request_json["payload"])
        # logging.info(f"payload - {payload}")
        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=7)
        # logging.info(f"new_time - {expires}")
        order = 122
        output = {
            # "status": "pending",
            #   "status": "invalid",
            "status": "valid",
            "expires": expires.isoformat() + "Z",
            "identifier": {"type": "dns", "value": "www.autok8s.xyz"},
            "challenges": [
                {
                    "type": "dns-01",
                    "url": f"{url}/challenge/{id}/http-01",
                    # "status": "pending",
                    "status": "valid",
                    "token": "def456",
                    "validation": "dns-txt-record-value",
                }
            ],
        }
        response = make_response(jsonify(output), 201)
        response.headers["Location"] = f"{url}/authz/{id}"
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response


class Order(Resource):
    def __init__(self):
        pass

    def post(sefl, id):
        request_json = request.get_json()

        protected = decode_base64_fix(request_json["protected"])
        # logging.info(f"protected - {protected}")

        payload = decode_base64_fix(request_json["payload"])
        # logging.info(f"payload - {payload}")
        # logging.info(f"id - {id}")
        return {
            "status": "valid",
            "certificate": "base64-encoded-certificate-data",
            "identifiers": [{"type": "dns", "value": "www.autok8s.xyz"}],
            "authorizations": [
                f"{url}/authz/1234567",
            ],
            "finalize": f"{url}/order/{id}/finalize",
            "certificate": f"{url}/certificate/{id}",
        }


class NewOrder(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl):
        request_json = request.get_json()

        protected = decode_base64_fix(request_json["protected"])
        # logging.info(f"protected - {protected}")

        payload = decode_base64_fix(request_json["payload"])
        # logging.info(f"payload - {payload}")
        current_time = datetime.now()

        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=7)
        # logging.info(f"new_time - {expires}")

        order = 122

        output = {
            "status": "pending",
            "expires": expires.isoformat() + "Z",
            "identifiers": [
                {"type": "dns", "value": "www.autok8s.xyz"},
            ],
            "authorizations": [
                f"{url}/authz/1234567",
            ],
            "finalize": f"{url}/order/{order}/finalize",
        }

        response = make_response(jsonify(output), 201)
        response.headers["Location"] = f"{url}/order/{order}"
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response

    def put(self):
        return "", 501


class NewNonce(Resource):
    def __init__(self):
        pass

    def head(self):
        response = Response()
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response

    def get(self):
        return "", 501

    def post(sefl):
        return "", 501

    def put(self):
        return "", 501


class AcmeChallenge(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl):
        return "", 501

    def put(self):
        return "", 501


class FinalizeOrder(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl, id):
        return {
            "status": "valid",
            "certificate": "base64-encoded-certificate-data",
            "identifiers": [{"type": "dns", "value": "www.autok8s.xyz"}],
            "authorizations": [
                f"{url}/authz/1234567",
            ],
            "finalize": f"{url}/order/{id}/finalize",
            "certificate": f"{url}/certificate/{id}",
        }


class Certs(Resource):
    def __init__(self):
        pass

    def post(self, id):
        cert_data = """-----BEGIN CERTIFICATE-----
MIIFIzCCAwugAwIBAgIUDky97RyxeKWJB4rvDfsTJd9kZGIwDQYJKoZIhvcNAQEL
BQAwGjEYMBYGA1UEAwwPSW50ZXJtaWRpYXRlIENBMB4XDTIzMDgyMjE5MzE1OVoX
DTMzMDgxOTE5MzE1OVowGDEWMBQGA1UEAwwNS3ViZXJuZXRlcyBDQTCCAiIwDQYJ
KoZIhvcNAQEBBQADggIPADCCAgoCggIBAMMrwapbJw70+qgm0QQJVatg3tdATdgF
4MEi72TDiC8oGxIytWBScadTa71Y8QvlzcG+fJ+mpA4rwcKpsItf4KwVCdUrcNeY
khQ7L7xD6eXWhQzsT2ef6qxw2uB8GCSg4dywao6jaKhj2hzvGSskI5kedhaCTnZ5
ljV7gf+mgIelRocQPr18Ht9KdEwWGZlyMiZTFF1Y/1vYGQsraM2FTCiXpsjxjKuf
4JG4D0ZLz/uHDcyyZWrgVX5/dLl5Lm1otkcYCnm/+hIJWZ8FDW89kcSjNRQMCB4s
Fyt3p6l0dCgMnNYglCX7Yujf0uFigF1LsKqXUnhOGMLXpVVDW8IQ++tpem28XQK5
FnuOO5uCsAxMd/Fx6JnbiODwcik5qh7nsqgd9ni32zuUs4zZgW7ruNFY8hBPO/6N
48cpD9/xNazx6BLL9U0qjimDSyo0ZcqgMbAolSuOu9+POd8oS1RKYuQQlTkie6WV
eutrlJ/LpSA2pUs1yPqq8e7e4pf4/i3jpNxNwE01rZLrD/256VmObdlqO/gjzNy8
JlgTAmyi0T/LAIgyUuOtNIRJm+y+a/s0HoYZNHPmJg5DqRDlUdvqY/GaVzvlBa1s
rI7MIV80vATl57w5aoFNOo0Ke5Pr6GSgScSwMbpNhN8XUY378lIdHAWXPOUzKbm1
8x3mN4dUKYPHAgMBAAGjYzBhMA4GA1UdDwEB/wQEAwICBDAPBgNVHRMBAf8EBTAD
AQH/MB0GA1UdDgQWBBT71G4KVH5Cf6zX77WjvhH/bu2fzDAfBgNVHSMEGDAWgBQv
BjzOxwPixFlQ1A5Q0wArF1jmaDANBgkqhkiG9w0BAQsFAAOCAgEAhQW2qX1lsjBf
NEniTOdIe2hyXWRhCWmLqhW2HBsY8WJchurMttmZ7vnkOxV39KNv14931CqzsJ1H
HDd3/tX4FvJXEX9kNzY9DDnCuOdm3vwn+w6+ifKZYljWOxcwW3VKF36r/MSR4AEG
Zf8lsEFym7j8OoCZELPs7btWEyjoupCOYto/AnESsrcrl7zKfj+gt4AoK3Tl+P4C
JD+eprl19jAqbhNvxFeF3ZT17lrq1yHG3FgRzTDpCasBH2fj09Rcy/9OtU4PplE7
0OIqfJtcQtuZG3iEO2HuizJ42iDTkm/ncEwd4eKjVxZYvXFDdmidxSBQtiZC36QQ
+KbnLkSCR3eD4bgaIumDA+NOTl+i9q6BqzMv3PersbnG7z8/y9N3Jyb2YxOTYueE
rJTUUCdy5o/Fqi68FSB/W2F2E4xEUguQENt1qAeNC8Zc2qiPS8P4rqQuwaiECUAn
czA4GdoKjSL3K3lLoFgXu/iwCM19zwFbAQZ/wo13Xuq49w3rNd+QXB92wZHcUBa/
qzsQeLGrixRMa4oygVkraLADwVLrQkB7tB0MdY5HOAJl8PAGMQGyv07FIkZlV+x4
M6h12zS61lYMmwR/DGfJlhGrIiYsaE7natwvR6pRI+HH5kEXPOwJYMvWrhV2zLRe
8r0+z2XVZJTOs+AXd3Na6pTI01qVnM0=
-----END CERTIFICATE-----"""  # Przykładowy certyfikat
        response = make_response(cert_data, 201)
        response.mimetype = "application/pem-certificate-chain"
        return response


class Finalize(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl, order_id):
        # Zwrócenie odpowiedzi z certyfikatem
        return {}, 501

    def put(self):
        return "", 501


class RevokeCert(Resource):
    def __init__(self):
        pass

    def get(self):
        return "", 501

    def post(sefl):
        return "", 501

    def put(self):
        return "", 501
