import dns.message

from constants import HEADER_BYTES_NUMBER
from dnspacket.DNS_answer import DNSAnswer
from dnspacket.DNS_header import DNSHeader
from dnspacket.DNS_query import DNSQuery


class DNSPacket:
    def __init__(self, data):
        self.__position = HEADER_BYTES_NUMBER
        self.header = self.get_header(data)
        self.queries = self.get_queries(data)
        self.answers = self.get_answers(data)

    def get_header(self, data):
        return DNSHeader(data)

    def get_queries(self, data):
        query = DNSQuery(data, self.__position)
        self.__position = query.position
        return query

    def get_answers(self, data):
        answers = []
        for i in range(self.header.ancount):
            answer = DNSAnswer(data, self.__position, self.queries.qname, self.queries.qtype, self.queries.qclass)
            answer.rdata = dns.message.from_wire(data).answer[0][i]
            answers.append(answer)
            self.__position = answer.position
        return answers
