class Disk:
    def __init__(self, disk) -> None:
        self.disk = disk
        self._parseDevice()

    def _parseDevice(self) -> None:
        self.path = self.disk.xpathEval("source/@file")[0].content
        self.bus = self.disk.xpathEval("address/@bus")[0].content.split("x")[1]
        self.domain = self.disk.xpathEval("address/@domain")[0].content.split("x")[1]
        self.fun = self.disk.xpathEval("address/@function")[0].content.split("x")[1]
        self.slot = self.disk.xpathEval("address/@slot")[0].content.split("x")[1]
        self.target_dev = self.disk.xpathEval("target/@dev")[0].content
        self.id = self.path.split("/")[5].split(".")[0]
        self.address = f"{self.domain}:{self.bus}:{self.slot}.{self.fun}"

    def ToJson(self) -> dict:
        return {
            "id": self.id,
            "path": self.path,
            "target": self.target_dev,
            "address": self.address,
        }

    def xml(self) -> str:
        xml = f"""
        <disk type='file' device='disk'>
            <driver name="qemu" type="qcow2"/>
            <source file='{self.path}'/>
            <target dev="{self.target_dev}" bus="virtio"/>
        </disk>
        """
        return xml
