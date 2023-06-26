from constants import COMPRESSED_LABEL_FIELD_SIZE, TTL_FIELD_SIZE, QTYPE_FIELD_SIZE, QCLASS_FIELD_SIZE, \
    RDLENGTH_FIELD_SIZE


class DNSAnswer:
    def __init__(self, data, position, qname, qtype, qclass):
        self.data = data
        self.name = qname
        self.type = qtype
        self.qclass = qclass
        self.position = position + COMPRESSED_LABEL_FIELD_SIZE + QTYPE_FIELD_SIZE + QCLASS_FIELD_SIZE
        self.ttl = self.get_ttl()
        self.rdlength = self.get_rdlength()
        self.rdata = self.get_rdata()

    def get_ttl(self):
        ttl = int.from_bytes(self.data[self.position:self.position + TTL_FIELD_SIZE], byteorder='big')
        self.position += TTL_FIELD_SIZE
        return ttl

    def get_rdlength(self):
        rdlength = int.from_bytes(self.data[self.position:self.position + RDLENGTH_FIELD_SIZE], byteorder='big')
        self.position += RDLENGTH_FIELD_SIZE
        return rdlength

    def get_rdata(self):
        self.position += self.rdlength
        return ''
