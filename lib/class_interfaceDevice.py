class InterfaceDevice:
    def __init__(self, network) -> None:
        self.network = network
        self._parseDevice()
        self.ip = None
        self.name = None

    def _parseDevice(self) -> None:
        self.mac = self.network.xpathEval("mac/@address")[0].content
        self.source = self.network.xpathEval("source/@network")[0].content
        self.model = self.network.xpathEval("model/@type")[0].content

        self.bus = self.network.xpathEval("address/@bus")[0].content.split("x")[1]
        self.domain = self.network.xpathEval("address/@domain")[0].content.split("x")[1]
        self.fun = self.network.xpathEval("address/@function")[0].content.split("x")[1]
        self.slot = self.network.xpathEval("address/@slot")[0].content.split("x")[1]
        self.address = f"{self.domain}:{self.bus}:{self.slot}.{self.fun}"

    def ToJson(self) -> dict:
        return {
            "mac": self.mac,
            "ip": self.ip,
            "name": self.name,
            "source": self.source,
            "model": self.model,
            "address": self.address,
        }

    def __str__(self):
        return self._ToJson()

    def __repr__(self):
        return self._ToJson()
