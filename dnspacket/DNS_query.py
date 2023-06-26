from constants import POINT, QTYPE_FIELD_SIZE, QCLASS_FIELD_SIZE, CLASS_VALUE
from dnspacket.type_values import type_values


class DNSQuery:
    def __init__(self, data, position):
        self.position = position
        self.data = data
        self.qname = self.get_qname()
        self.qtype = self.get_qtype()
        self.qclass = self.get_qclass()

    def get_qname(self):
        label_length = self.data[self.position] & 0b111111
        qname = ''
        while label_length:
            self.position += 1
            qname += (self.data[self.position:self.position + label_length]).decode() + POINT
            self.position += label_length
            label_length = self.data[self.position]
        self.position += 1
        return qname[:-1]

    def get_qtype(self):
        qtype = type_values[int.from_bytes(self.data[self.position:self.position + QTYPE_FIELD_SIZE], byteorder='big')]
        self.position += QTYPE_FIELD_SIZE
        return qtype

    def get_qclass(self):
        self.position += QCLASS_FIELD_SIZE
        return CLASS_VALUE
