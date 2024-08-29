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

    def __init__(self, identifiers) -> None:
        self.identifiers = sorted(identifiers, key=lambda x: (x["type"], x["value"]))
        self.order = self.__load()
        if not self.order:
            self.__create()

    def __load(self):
        return False

    def __create(self) -> None:
        current_time = datetime.utcnow()
        expires = current_time + timedelta(days=VALID_CRT_DAYS)
        authz_array = []
        authz_model_array = []

        for identifier in self.identifiers:
            authz = Authorization(identifier).getMongo()
            authz_model_array.append(authz)

        self.order = OrderModel(
            status=StatusOrder.PENDING.value,
            identifiers=self.identifiers,
            expires=expires.isoformat() + "Z",
            authorizations=authz_model_array,
        )
        self.is_new = True

    def isNew(self):
        return self.is_new

    def output(self):
        return self.order

    def json(self):
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


class Account:
    @property
    def id(self):
        if self.account:
            return self.account.id

        return self._id

    @property
    def status(self):
        if self.account:
            return self.account.status

        return None

    @property
    def contact(self):
        if self.account:
            return self.account.contact

        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = value

    @id.setter
    def id(self, value):
        self._id = value

    def __init__(
        self,
        id=None,
        jwk=None,
        contact=None,
        onlyReturnExisting=False,
        termsOfServiceAgreed=None,
    ) -> None:
        self.jwk = jwk
        self.id = id
        self.contact = contact
        self.account = None
        self.termsOfServiceAgreed = termsOfServiceAgreed
        self.newAccount = False

        self.__load()
        if not self.account and not onlyReturnExisting:
            self.newAccount = True
            self.__create()

    def __load(self):
        if self.id:
            query = {"id": self.id}
        else:
            query = {"jwk": self.jwk}

        self.account = AccountModel.objects(**query).first()

    def __create(self) -> None:
        self.account = AccountModel(
            contact=self._contact,
            termsOfServiceAgreed=self.termsOfServiceAgreed,
            jwk=self.jwk,
        )
        self.account.save()

    def NewOrder(self, identifiers):
        order = Order(identifiers=identifiers)
        self.account.update(orders=[order.output()])
        return order
