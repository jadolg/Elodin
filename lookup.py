import dns.resolver


def resolve(domain):
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['172.26.0.11', '172.17.16.11',]
    try:
        r = dns.resolver.query(domain, 'a')
        return r.rrset.items[0]
    except:
        return False