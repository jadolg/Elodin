#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import socket

import os
from threading import Thread
import dns.resolver

from Elodin.settings import LOCK_FILE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Elodin.settings')
import django
django.setup()
from NamesDatabase.models import Name, Log

ALTERNATIVES = ['10.24.18.10',
                '10.31.18.2',
                '192.168.192.1',
                '192.168.32.1',
                '192.168.32.4',
                '192.168.204.2',
                '10.16.1.1',
                '10.24.0.1',
                '10.30.1.1',
                '192.168.128.1',
                '10.26.1.1',
                '10.22.1.1']

# ALTERNATIVES = ['172.26.0.11', '172.17.16.11',]

class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.dominio = ''

        tipo = (ord(data[2]) >> 3) & 15  # Opcode bits
        if tipo == 0:  # Standard query
            ini = 12
            lon = ord(data[ini])
            while lon != 0:
                self.dominio += data[ini + 1:ini + lon + 1] + '.'
                ini += lon + 1
                lon = ord(data[ini])

    def respuesta(self, ip):
        packet = ''
        if self.dominio:
            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += '\xc0\x0c'  # Pointer to domain name
            packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += str.join('', map(lambda x: chr(int(x)), ip.split('.')))  # 4bytes of IP
        return packet


def resolve(domain):
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ALTERNATIVES
    try:
        r = dns.resolver.query(domain, 'a')
        print 'resolved',r.rrset.items[0]
        return str(r.rrset.items[0])
    except:
        return False


def handle(udps, data, addr):
    ip = '127.0.0.1'
    p = DNSQuery(data)
    direccion = Name.objects.filter(nombre=p.dominio)
    if len(direccion) > 0:
        print 'encontrado', direccion[0]
        ip = direccion[0].ip
    else:
        print 'no encontrado', p.dominio

        aux_ip = resolve(p.dominio)
        if aux_ip and aux_ip != '127.0.0.1':
            ip = aux_ip
            if len(Name.objects.filter(nombre=p.dominio+'.')) == 0:
                try:
                    Name(nombre=p.dominio, ip=ip).save()
                    Log(usuario='system', accion='agregar', nombre=p.dominio, ip=ip, ip_usuario='127.0.0.1').save()
                except:
                    pass


    udps.sendto(p.respuesta(ip), addr)

    print 'Respuesta a %s: %s -> %s' % (addr, p.dominio, ip)


def main():
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('', 53))
    lock_file = open(LOCK_FILE, 'w')
    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            Thread(target=handle, args=(udps, data, addr)).start()

    except KeyboardInterrupt:
        print 'Finalizando'
        udps.close()
    finally:
        lock_file.close()
        os.unlink(LOCK_FILE)

if __name__ == '__main__':
    main()
