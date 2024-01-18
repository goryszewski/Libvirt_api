import libvirt, libxml2

def flat_list(vms):
    result = []
    for vm in vms:
        try:
            xmldesc =vm.XMLDesc(0)
            doc = libxml2.parseDoc(xmldesc).xpathNewContext()
            VM=doc.xpathEval("/domain/name")[0].content
        except:
            continue
        result.append(VM)

    return result

class Libvirt:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")
    def get(self):
        result = []
        vms = self.conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
        result = flat_list(vms)

        return result
