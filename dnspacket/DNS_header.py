class DNSHeader:
    def __init__(self, header):
        self.id = int.from_bytes(header[:2], byteorder='big')
        self.qr = (header[2] >> 7) & 1
        self.opcode = (header[2] >> 3) & 0b1111
        self.aa = (header[2] >> 2) & 0b1 if self.qr else None
        self.tc = (header[2] >> 1) & 0b1
        self.rd = header[2] & 0b1
        self.ra = (header[3] >> 7) & 0b1 if self.qr else None
        self.rcode = header[3] & 0b1111 if self.qr else None
        self.qdcount = int.from_bytes(header[4:6], byteorder='big')
        self.ancount = int.from_bytes(header[6:8], byteorder='big')
        self.nscount = int.from_bytes(header[8:10], byteorder='big')
        self.arcount = int.from_bytes(header[10:12], byteorder='big')
