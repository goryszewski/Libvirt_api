import libvirt
import libxml2
from typing import List

TARGET_DEV_DISK = ["vdb", "vdc", "vdd", "vde", "vdf", "vdg", "vdh", "vdi"]


def desc(vm):
    xmldesc = vm.XMLDesc(0)
    doc = libxml2.parseDoc(xmldesc).xpathNewContext()
    return doc.xpathEval("/domain/description")


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

        self.address = f"{self.domain}:{self.bus}:{self.slot}:{self.fun}"

    def ToJson(self) -> dict:
        return {"path": self.path, "target": self.target_dev, "address": self.address}

    def xml(self) -> str:
        xml = f"""
        <disk type='file' device='disk'>
            <driver name="qemu" type="qcow2"/>
            <source file='{self.path}'/>
            <target dev="{self.target_dev}" bus="virtio"/>
        </disk>
        """
        return xml


class VM:
    def __init__(self, vm: libvirt.virDomain) -> None:
        self.vm = vm

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

    def AttachDisk(self, hdd_id: str) -> bool:
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
        return True

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


class Libvirt:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")


    def getByName(self, name):
        vms = self.conn.listAllDomains(0)
        for vm in vms:
            if vm.name() == name:
                return VM(vm)


    def get(self):
        result = []
        vms = self.conn.listAllDomains(0)

        for vm in vms:
            tmp = desc(vm)
            if not tmp:
                continue
            elif not "nodeK8S" in tmp[0].content:
                continue

            vmx = {"status": 0}
            vmx["id"] = vm.ID()
            vmx["name"] = vm.name()
            vmx["OSType"] = vm.OSType()
            vmx["hasCurrentSnapshot"] = vm.hasCurrentSnapshot()
            if vm.isActive():
                vmx["hostname"] = vm.hostname()
                vmx["time"] = vm.getTime()
                vmx["status"] = "1"
                vmx["net"] = vm.interfaceAddresses(
                    libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0
                )

            vmx["state"] = vm.state()  # ​state, reason
            vmx["info"] = vm.info()  # ​state, maxmem, mem, cpus, cput

            result.append(vmx)

        return result

    def create(self, payload):
        payload = """
        <domain type='kvm'><name>{name}</name><memory>500000</memory><vcpu>{cpu}</vcpu>  <memory unit="KiB">{memory}</memory>
        <currentMemory unit="KiB">{memory}</currentMemory><os><type arch='x86_64' machine='pc'>hvm</type><boot dev='hd'/><boot dev='cdrom'/></os></domain>
        """.format(
            **payload
        )
        dom = self.conn.defineXMLFlags(payload, 0)
        if dom.create() < 0:
            return "", 500
        return "Done", 200

    def delete(self, name):
        domain = self.conn.lookupByName(name)
        domain.destroy()
        domain.undefine()
