import libvirt
from typing import List

from .Base import desc
from .class_vm import VM


class Libvirt:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")

    def getVmByName(self, name) -> VM:
        vms = self.GetVms()
        for vm in vms:
            if vm.name == name:
                return vm
        return None


    def GetVms(self) -> List[VM]:
        output = []
        vms = self.conn.listAllDomains(0)
        for vm in vms:
            tmp = desc(vm)
            if not tmp:
                continue
            elif not "nodeK8S" in tmp[0].content:
                continue

            output.append(VM(vm))
        return output

    def get(self): # DEP
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
