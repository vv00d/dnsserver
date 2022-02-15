from scapy.all import *


def get_ip(uri):
    answer = sr1(IP(dst="127.0.0.1")/UDP(dport=53) /
                 DNS(rd=1, qd=DNSQR(qname=uri)), verbose=0)
    return answer[DNS].summary()


print(get_ip("google.com"))
print(get_ip("abcd.com"))
