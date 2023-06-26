import socket

import dns.resolver

from cache_methods import is_in_cache, get_from_cache, add_to_cache
from constants import PORT, LOCALHOST, BUFSIZE


class DNSServer:
    def __init__(self):
        self.__default_server = dns.resolver.get_default_resolver().nameservers[0]
        self.__localhost_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__default_server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.__localhost_sock.bind((LOCALHOST, PORT))
        while True:
            qdata, qaddr = self.__localhost_sock.recvfrom(BUFSIZE)
            adata = self.__resolve(qdata)
            self.__localhost_sock.sendto(adata, qaddr)

    def __resolve(self, qdata):
        if is_in_cache(qdata):
            return self.__build_answer(qdata, get_from_cache(qdata))
        self.__default_server_sock.sendto(qdata, (self.__default_server, PORT))
        adata, _ = self.__default_server_sock.recvfrom(BUFSIZE)
        add_to_cache(adata)
        return adata

    @staticmethod
    def __build_answer(qdata, adata):
        response = dns.message.make_response(dns.message.from_wire(qdata))
        name = response.question[0].name
        rdataclass = response.question[0].rdclass
        rdatatype = response.question[0].rdtype
        response.answer.append(dns.rrset.RRset(name, rdataclass, rdatatype))
        for i in adata:
            answer = dns.rdata.from_text(rdataclass, rdatatype, i[0])
            response.answer[-1].add(answer)
        return response.to_wire()
