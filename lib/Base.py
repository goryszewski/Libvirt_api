import libxml2

TARGET_DEV_DISK = ["vdb", "vdc", "vdd", "vde", "vdf", "vdg", "vdh", "vdi"]


class Iterable:
    def __init__(self) -> None:
        self.i = 0
        self.aggregation = []

    def __iter__(self):
        return self

    def __next__(self):
        internal_indicator = self.i

        if internal_indicator < len(self.aggregation):
            self.i += 1
            return self.aggregation[internal_indicator]
        self.i = 0

        raise StopIteration


def desc(vm):
    xmldesc = vm.XMLDesc(0)
    doc = libxml2.parseDoc(xmldesc).xpathNewContext()
    return doc.xpathEval("/domain/description")
