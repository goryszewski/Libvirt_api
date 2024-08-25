from Model.Acme import *
from datetime import datetime, timedelta
from .tools import *
import uuid
import base64, json

VALID_CRT_DAYS = 30
URL_SERVER = "http://10.17.3.1:8050/acme"


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


class Order:
    @property
    def id(self):
        return self.order.id

    def __init__(self, kid, identifiers) -> None:
        self.account_id = kid.split("/")[-1]
        self.identifiers = sorted(identifiers, key=lambda x: (x["type"], x["value"]))
        self.__create()

    def __create(self) -> None:
        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=VALID_CRT_DAYS)
        authz_array = []
        authz_model_array = []
        # identifiers = to_json(order.identifiers)
        for identifier in self.identifiers:
            authz = Authorization(identifier).getMongo()
            authz_model_array.append(authz)

        self.order = OrderModel(
            accountid=self.account_id,
            status="pending",
            identifiers=self.identifiers,
            expires=expires.isoformat() + "Z",
            authorizations=authz_model_array,
        )

        self.order.save()

    def output(self) -> dict:
        return {
            "status": self.order.status,
            "expires": self.order.expires,
            "identifiers": to_json(self.order.identifiers),
            "authorizations": [],
            "finalize": f"{URL_SERVER}/order/{self.order.id}/finalize",
        }


class Authorization:
    def __init__(self, identifier) -> None:
        self.identifier = identifier
        self.__create()

    def __create(self) -> None:
        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=VALID_CRT_DAYS)
        self.authz = AuthorizationModel(
            status="pending",
            expires=expires.isoformat() + "Z",
            identifier=self.identifier,
            challenges=[Challenge().getMongo()],
            wildcard=False,
        )

    def getMongo(self):
        return self.authz

    # authz_array.append(f"{URL_SERVER}/order/{order.id}/authz/{authz.authz_id}")


class Challenge:
    def __init__(self) -> None:
        self.__create()

    def __create(self, challenage_type="http-01") -> None:
        self.challenge = ChallengeModel(
            type=challenage_type,
            status="pending",
            token=str(uuid.uuid4()),
            validation="dns-txt-record-value",
        )

    def getMongo(self):
        return self.challenge
