import libvirt

class Libvirt:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")
    def get(self):
        result = []
        vms = self.conn.listAllDomains(0)
        print(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
        for vm in vms:
            vmx={"status":0}
            vmx['id']=vm.ID()
            vmx['name']=vm.name()
            vmx['OSType']=vm.OSType()
            vmx['hasCurrentSnapshot']=vm.hasCurrentSnapshot()
            if vm.isActive():
                vmx['hostname']=vm.hostname()
                vmx['time']=vm.getTime()
                vmx['status']='1'
            vmx['state'] = vm.state() # ​state, reason
            vmx['info'] = vm.info()
            result.append(vmx)

        return result

    def create(self,payload):
        payload = """
        <domain type='kvm'><name>{name}</name><memory>500000</memory><vcpu>{cpu}</vcpu>  <memory unit="KiB">{memory}</memory>
        <currentMemory unit="KiB">{memory}</currentMemory><os><type arch='x86_64' machine='pc'>hvm</type><boot dev='hd'/><boot dev='cdrom'/></os></domain>
        """.format(**payload)
        dom = self.conn.defineXMLFlags(payload, 0)
        if dom.create() < 0:
            return '',500
        return "Done",200

    def delete(self,name):
        domain = self.conn.lookupByName(name)
        domain.destroy()
        domain.undefine()
