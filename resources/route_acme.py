from .acme import *


def route_acme(api):
    api.add_resource(Directory, "/acme/directory")  # Get
    api.add_resource(NewAccount, "/acme/new-account")  # POST
    api.add_resource(NewNonce, "/acme/new-nonce")
    api.add_resource(AuthZ, "/acme/authz/<id>")
    api.add_resource(Order, "/acme/order/<id>")
    api.add_resource(Certs, "/acme/certificate/<id>")
    api.add_resource(FinalizeOrder, "/acme/order/<id>/finalize")
    api.add_resource(NewOrder, "/acme/new-order")  # POST
    api.add_resource(AcmeChallenge, "/.well-known/acme-challenge/<token>")  # GET
    api.add_resource(Finalize, "/acme/finalize/<order_id>")  # POST
    api.add_resource(RevokeCert, "/acme/revoke-cert")  # POST


# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "GET /acme/directory HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "POST /acme/new-account HTTP/1.1" 201 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "POST /acme/new-order HTTP/1.1" 201 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:24 INFO     10.17.3.152 - - [05/Aug/2024 20:15:24] "POST /acme/authz/1234567 HTTP/1.1" 201 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "GET /acme/directory HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "POST /acme/new-account HTTP/1.1" 201 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "POST /acme/order/122 HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "POST /acme/authz/1234567 HTTP/1.1" 201 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "POST /acme/order/122/finalize HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "POST /acme/order/122 HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:25 INFO     10.17.3.152 - - [05/Aug/2024 20:15:25] "HEAD /acme/new-nonce HTTP/1.1" 200 -
# api-1            | 2024-08-05 20:15:26 INFO     10.17.3.152 - - [05/Aug/2024 20:15:26] "POST /acme/certificate/122 HTTP/1.1" 201 -
