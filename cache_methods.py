import json
from datetime import datetime

from dnspacket.DNS_packet import DNSPacket


def is_in_cache(qdata):
    dns_packet = DNSPacket(qdata)
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    if dns_packet.queries.qname in cache:
        if dns_packet.queries.qtype in cache[dns_packet.queries.qname]:
            for rdata in cache[dns_packet.queries.qname][dns_packet.queries.qtype]:
                if rdata[2] + rdata[1] < datetime.now().timestamp():
                    remove_from_cache(dns_packet.queries.qname, dns_packet.queries.qtype)
                    return False
            else:
                return True
    return False


def get_from_cache(qdata):
    with open('cache.json', 'rb') as f:
        cache = json.load(f)
    dns_packet = DNSPacket(qdata)
    print('Loaded from cache')
    adata = cache[dns_packet.queries.qname][dns_packet.queries.qtype]
    return adata


def remove_from_cache(name, qtype):
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    del cache[name][qtype]
    with open('cache.json', 'w') as f:
        json.dump(cache, f)


def add_to_cache(adata):
    with open('cache.json', 'r') as f:
        cache = json.load(f)
    dns_packet = DNSPacket(adata)
    name = dns_packet.queries.qname
    if name not in cache:
        cache[name] = {}
    for answer in dns_packet.answers:
        if answer.type not in cache[name]:
            cache[name][answer.type] = []
        cache[name][answer.type].append((str(answer.rdata), answer.ttl, datetime.now().timestamp()))
    with open('cache.json', 'w') as f:
        json.dump(cache, f)
