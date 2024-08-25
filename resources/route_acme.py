from .acme import *


def route_acme(api):
    api.add_resource(Directory, "/acme/directory")  # Get
    api.add_resource(NewAccount, "/acme/account")  # POST
    api.add_resource(Account, "/acme/account/<id>")
    api.add_resource(NewNonce, "/acme/new-nonce")

    api.add_resource(AcmeChallenge, "/.well-known/acme-challenge/<token>")  # GET
    api.add_resource(RevokeCert, "/acme/revoke-cert")  # POST

    # api.add_resource(NewOrder, "/acme/new-order")  # POST
    # api.add_resource(Order, "/acme/order/<id>")
    # api.add_resource(FinalizeOrder, "/acme/order/<id>/finalize")
    # api.add_resource(AuthZ, "/acme/authz/<id>")
    # api.add_resource(Challenge, "/acme/challenge/<authz_id>/<type>")
    # api.add_resource(Certs, "/acme/certificate/<id>")

    #  new route

    api.add_resource(NewOrder, "/acme/order")
    api.add_resource(Order, "/acme/order/<order_id>")
    api.add_resource(FinalizeOrder, "/acme/order/<order_id>/finalize")
    api.add_resource(AuthZ, "/acme/order/<order_id>/authz/<authz_id>")
    api.add_resource(
        Challenge,
        "/acme/order/<order_id>/authz/<authz_id>/challenge/<challenge_id>/<type>",
    )
    api.add_resource(Certs, "/acme/order/<order_id>/certificate/<certificate_id>")


# api-1            | 2024-08-08 23:36:56 INFO     10.17.3.152 - - [08/Aug/2024 23:36:56] "GET /acme/directory HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:56 INFO     10.17.3.152 - - [08/Aug/2024 23:36:56] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:56 INFO     10.17.3.152 - - [08/Aug/2024 23:36:56] "POST /acme/new-account HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:56 INFO     10.17.3.152 - - [08/Aug/2024 23:36:56] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:56 INFO     10.17.3.152 - - [08/Aug/2024 23:36:56] "POST /acme/new-order HTTP/1.1" 201 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "POST /acme/authz/66b5ff583159c75e6ec5b274 HTTP/1.1" 201 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "GET /acme/directory HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "POST /acme/new-account HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "POST /acme/order/66b5ff583159c75e6ec5b273 HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:57 INFO     10.17.3.152 - - [08/Aug/2024 23:36:57] "POST /acme/authz/66b5ff583159c75e6ec5b274 HTTP/1.1" 201 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "POST /acme/order/66b5ff583159c75e6ec5b273/finalize HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "POST /acme/order/66b5ff583159c75e6ec5b273 HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-08 23:36:58 INFO     10.17.3.152 - - [08/Aug/2024 23:36:58] "POST /acme/certificate/66b5ff583159c75e6ec5b273 HTTP/1.1" 201 -
