class Cert:
    '无人艇的证书'
    cert_count = 0

    def __init__(self, master_addr, domain_id, device_id, device_addr, sig):
        self.master_addr = master_addr
        self.domain_id = domain_id
        self.device_id = device_id
        self.device_addr = device_addr
        self.sig = sig
        Cert.cert_count += 1
