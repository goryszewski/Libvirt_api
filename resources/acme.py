from flask_restful import Resource
from flask import request, jsonify, Response, make_response
import base64, json
from lib.logging import logging
from lib.ca import sign_certificate_request
from datetime import datetime, timedelta

from Model.AcmeAccount import (
    AccountModel,
    AccountProtectSchema,
    AccountPayloadSchema,
    RequestOrderSchema,
    OrderModel,
    AuthorizationModel,
    CertModel,
)


URL_SERVER = "http://10.17.3.1:8050/acme"
VALID_CRT_DAYS = 30


def decode_base64_fix(data):
    fix = "=" * int(len(data) % 4)
    payload = base64.b64decode(data + fix)
    return payload.decode()


def to_json(items):
    output = []
    for item in items:
        tmp = json.loads(item.to_json())
        if "_id" in tmp:
            del tmp["_id"]
        if "objectid" in tmp:
            del tmp["objectid"]
        output.append(tmp)
    return output


class Directory(Resource):
    def __init__(self):
        pass

    def get(self):
        output = {
            "newNonce": f"{URL_SERVER}/new-nonce",
            "newAccount": f"{URL_SERVER}/new-account",
            "newOrder": f"{URL_SERVER}/new-order",
            "revokeCert": f"{URL_SERVER}/revoke-cert",
            "keyChange": f"{URL_SERVER}/key-change",
        }
        return output, 200

    def post(sefl):
        return "", 501

    def put(self):
        return "", 501


class Account(Resource):
    def __init__(self):
        pass

    def post(self, id):
        headers = dict(request.headers)
        logging.info(f" [Account] - headers : {headers}")

        account = AccountModel.objects(id=id).first()
        if account:
            output = {
                "status": account.status,
                "contact": account.contact,
                "termsOfServiceAgreed": account.termsOfServiceAgreed,
                "orders": f"{URL_SERVER}/account/{account.id}/orders",
            }
            response = make_response(jsonify(output), 200)
            return response
        else:
            output = {
                "type": "urn:ietf:params:acme:error:accountDoesNotExist",
                "detail": f"Account with ID {id} does not exist",
                "status": 404,
            }
            return output, 404


class NewAccount(Resource):
    def __init__(self):
        self.account_payload_schema = AccountPayloadSchema()
        self.account_protect_schema = AccountProtectSchema()

    def get(self):
        return "", 501

    def post(self):
        request_json = request.get_json()
        headers = dict(request.headers)
        logging.info(f" [NewAccount] - headers : {headers}")

        protected = json.loads(decode_base64_fix(request_json["protected"]))
        logging.info(f" [NewAccount] - protected : {protected}")

        error = self.account_protect_schema.validate(protected)
        if error:
            logging.error(f"1: {error}")
            return error, 422

        payload = json.loads(decode_base64_fix(request_json["payload"]))
        error = self.account_payload_schema.validate(payload)
        if error:
            logging.error(f"2: {error}")
            return error, 422

        logging.info(f" [NewAccount] - payload : {payload}")

        account = AccountModel.objects(jwk=protected["jwk"]["n"]).first()

        rc = 501
        if account:
            rc = 200
        else:
            if "onlyReturnExisting" in payload and payload["onlyReturnExisting"]:
                output = {
                    "type": "urn:ietf:params:acme:error:accountDoesNotExist",
                    "detail": "No account exists with the provided key",
                    "status": 400,
                }
                return output, 400
            rc = 201
            account = AccountModel(
                **self.account_payload_schema.dump(payload), jwk=protected["jwk"]["n"]
            )
            account.save()

        output = {
            "contact": account.contact,
            "status": "valid",
            "orders": f"{URL_SERVER}/account/{account.id}/orders",
        }
        response = make_response(jsonify(output), rc)
        response.headers["Location"] = f"{URL_SERVER}/account/{account.id}"
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
        authz = AuthorizationModel.objects(id=id).first()

        output = {
            "status": authz.status,
            "expires": authz.expires,
            "identifier": authz.identifier,
            "challenges": authz.challenges,
        }
        logging.debug(f"[AuthZ] output - {output}")

        response = make_response(jsonify(output), 201)
        response.headers["Location"] = f"{URL_SERVER}/authz/{id}"
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response


class Order(Resource):
    def __init__(self):
        pass

    def post(sefl, id):
        authorizations_array = []

        order = OrderModel.objects(id=id).first()
        authorizations = AuthorizationModel.objects(orderid=str(order.id))
        for athz in authorizations:
            authorizations_array.append(
                f"{URL_SERVER}/authz/{athz.id}",
            )

        output = {
            "status": "valid",
            "certificate": "base64-encoded-certificate-data",
            "identifiers": to_json(order.identifiers),
            "authorizations": authorizations_array,
            "finalize": f"{URL_SERVER}/order/{order.id}/finalize",
            "certificate": f"{URL_SERVER}/certificate/{order.id}",
        }
        logging.debug(f"[Order] output - {output}")

        response = make_response(output, 200)
        response.headers["Location"] = f"{URL_SERVER}/order/{order.id}"
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response


class NewOrder(Resource):
    def __init__(self):
        self.order_schema = RequestOrderSchema()

    def get(self):
        return "", 501

    def post(self):
        request_json = request.get_json()

        protected = decode_base64_fix(request_json["protected"])
        logging.debug(f"[NewOrder] protected - {protected}")

        payload = json.loads(decode_base64_fix(request_json["payload"]))
        logging.debug(f"[NewOrder] payload - {payload}")

        error = self.order_schema.validate(payload)
        if error:
            logging.error(error)
            return error, 500
        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=VALID_CRT_DAYS)

        rc = 501
        order = OrderModel.objects(**payload).first()
        if order:
            rc = 201
        else:
            order = OrderModel(
                **self.order_schema.dump(payload),
                status="valid",
                expires=expires.isoformat() + "Z",
            )
            order.save()
            rc = 201

        # create authorizations
        authz_array = []
        challenges_array = []
        identifiers = to_json(order.identifiers)
        for identifier in identifiers:
            challenge = {
                "url": f"{URL_SERVER}/challenge/{order.id}/http-01",
                "type": "http-01",
                "status": "valid",
                "token": "def456",
                "validation": "dns-txt-record-value",
            }
            challenges_array.append(challenge)

            authz = AuthorizationModel(
                orderid=str(order.id),
                status="valid",
                expires=expires.isoformat() + "Z",
                identifier=identifier,
                challenges=challenges_array,
                wildcard=False,
            )
            authz.save()
            authz_array.append(f"{URL_SERVER}/authz/{authz.id}")

        output = {
            "status": order.status,
            "expires": order.expires,
            "identifiers": to_json(order.identifiers),
            "authorizations": authz_array,
            "finalize": f"{URL_SERVER}/order/{order.id}/finalize",
        }
        logging.debug(f"[NewOrder] output - {output}")

        response = make_response(jsonify(output), rc)
        response.headers["Location"] = f"{URL_SERVER}/order/{order.id}"
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
        request_json = request.get_json()

        protected = decode_base64_fix(request_json["protected"])
        logging.debug(f"[FinalizeOrder] protected - {protected}")

        payload = json.loads(decode_base64_fix(request_json["payload"]))
        logging.debug(f"[FinalizeOrder] payload - {payload}")
        authorizations_array = []

        test = sign_certificate_request(payload["csr"])

        order = OrderModel.objects(id=id).first()
        authorizations = AuthorizationModel.objects(orderid=str(order.id))

        crt = CertModel(orderid=str(order.id), cert=test)
        crt.save()

        for athz in authorizations:
            authorizations_array.append(
                f"{URL_SERVER}/authz/{athz.id}",
            )
        output = {
            "status": "valid",
            "certificate": "base64-encoded-certificate-data",
            "identifiers": to_json(order.identifiers),
            "authorizations": authorizations_array,
            "finalize": f"{URL_SERVER}/order/{order.id}/finalize",
            "certificate": f"{URL_SERVER}/certificate/{order.id}",
        }
        response = make_response(jsonify(output), 200)
        response.headers["Replay-Nonce"] = "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8"
        return response


class Certs(Resource):
    def __init__(self):
        pass

    def post(self, id):
        rc = 404
        output = ""

        cert_data = CertModel.objects(orderid=str(id)).first()
        if cert_data:
            rc = 201
            output = cert_data.cert

        response = make_response(output, rc)
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
