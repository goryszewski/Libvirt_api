import libvirt
import libxml2
from typing import List

from .Base import TARGET_DEV_DISK
from .class_disk import Disk
from .class_interfaceDevice import InterfaceDevice


class VM:
    def __init__(self, vm: libvirt.virDomain) -> None:
        self.vm = vm
        self._parseVM()

    def _parseVM(self) -> None:
        self.id = self.vm.ID()
        self.name = self.vm.name()
        self.OSType = self.vm.OSType()
        self.hasCurrentSnapshot = self.vm.hasCurrentSnapshot()
        self.net = []
        self.n = self.getNetworks()

        if self.vm.isActive():
            self.hostname = self.vm.hostname()
            self.time = self.vm.getTime()
            self.net = self._PrepNetwork()

        self.state = self.vm.state()  # ​state, reason
        self.info = self.vm.info()  # ​state, maxmem, mem, cpus, cput

    def _PrepNetwork(self) -> None:
        for network in self.n:
            for name, value in self.vm.interfaceAddresses(
                libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0
            ).items():
                if value["hwaddr"] == network.mac:
                    network.ip = value["addrs"][0]["addr"]
                    network.name = name

    def ToJson(self):
        output = {
            "id": self.id,
            "name": self.name,
            "interface": [item.ToJson() for item in self.n],
            "type": self.OSType,
            "disks": [disk.ToJson() for disk in self.getDisks()],
        }

        return output

    def getDiskByPath(self, path: str) -> Disk:
        disks = self.getDisks()
        for disk in disks:
            if disk.path == path:
                return disk
        return None

    def DetachDisk(self, hdd_id: str) -> bool:
        path = f"/var/lib/libvirt/images/{hdd_id}.qcow2"
        disk = self.getDiskByPath(path)
        if not disk:
            return None

        xml = disk.xml()

        self.vm.detachDevice(xml)

        return True

    def IsDiskAttach(self, hdd_id: str) -> bool:
        path = f"/var/lib/libvirt/images/{hdd_id}.qcow2"
        if self.getDiskByPath(path):
            return True
        return False

    def AttachDisk(self, hdd_id: str) -> Disk:
        if self.IsDiskAttach(hdd_id):
            return False

        target_dev = self._getFreeTarget()
        if not target_dev:
            return False
        path = f"/var/lib/libvirt/images/{hdd_id}.qcow2"

        xml = f"""
        <disk type='file' device='disk'>
            <driver name="qemu" type="qcow2"/>
            <source file='{path}'/>
            <target dev="{target_dev}" bus="virtio"/>
        </disk>
        """
        self.vm.attachDevice(xml)
        path = f"/var/lib/libvirt/images/{hdd_id}.qcow2"
        disk = self.getDiskByPath(path)
        return disk

    def getDisks(self) -> List[Disk]:
        output = []
        xml = self._preXml()
        disks = xml.xpathEval(f"devices/disk")
        for disk in disks:
            file = disk.xpathEval("source/@file")
            if not file:
                continue
            output.append(Disk(disk))
        return output

    def getNetworks(self) -> List[InterfaceDevice]:
        output = []
        xml = self._preXml()
        networkdevices = xml.xpathEval(f'devices/interface[@type="network"]')
        for networkdevice in networkdevices:
            output.append(InterfaceDevice(networkdevice))
        return output

    def getDisksJson(self) -> list:
        disks = self.getDisks()
        output = []
        for disk in disks:
            output.append(disk.ToJson())
        return output

    def _getFreeTarget(self) -> str:
        disks = self.getDisks()
        listdev = []

        for item in disks:
            listdev.append(item.target_dev)

        for item in TARGET_DEV_DISK:
            if not item in listdev:
                return item
        return None

    def _preXml(self) -> libxml2.xmlNode:
        xmldesc = self.vm.XMLDesc(0)
        doc = libxml2.parseDoc(xmldesc).xpathNewContext()

        return doc.xpathEval("/domain")[0]
