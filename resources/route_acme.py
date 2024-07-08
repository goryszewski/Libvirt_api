from .acme import *

def route_acme(api):
    api.add_resource(Directory, "/acme/directory") # Get
    api.add_resource(NewAccount, "/acme/new-account") # POST
    api.add_resource(NewOrder,"/acme/new-order") #POST
    api.add_resource(AcmeChallenge,"/.well-known/acme-challenge/<token>") #GET
    api.add_resource(Finalize,"/acme/finalize/<order_id>") #POST
    api.add_resource(RevokeCert,"/acme/revoke-cert") #POST
