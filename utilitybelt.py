"""
 _   _ _   _ _ _ _          ______      _ _
| | | | | (_) (_) |         | ___ \    | | |
| | | | |_ _| |_| |_ _   _  | |_/ / ___| | |_
| | | | __| | | | __| | | | | ___ \/ _ \ | __|
| |_| | |_| | | | |_| |_| | | |_/ /  __/ | |_
 \___/ \__|_|_|_|\__|\__, | \____/ \___|_|\__|
                      __/ |
                     |___/

A library to make you a Python CND Batman
"""

import GeoIP
import requests
import json, re, socket
import socket
import struct

gi = GeoIP.open("./data/GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)

def ip_to_long(ip):
    """Convert an IPv4Address string to long"""
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

def ip_between(ip, start, finish):
    """Checks to see if IP is between start and finish"""

    if is_IPv4Address(ip) and is_IPv4Address(start) and is_IPv4Address(finish):
        ip_long = ip_to_long(ip)
        start_long = ip_to_long(start)
        finish_long = ip_to_long(finish)

        if start_long <= ip_long <= finish_long:
            return True
        else:
            return False
    else:
        return False

def is_rfc1918(ip):
    if ip_between(ip, "10.0.0.0", "10.255.255.255"):
        return True
    elif ip_between(ip, "172.16.0.0", "172.31.255.255"):
        return True
    elif ip_between(ip, "192.168.0.0", "192.168.255.255"):
        return True
    else:
        return False

def is_IPv4Address(ipv4address):
    """Returns true for valid IPv4 Addresses, false for invalid."""

    ip_regex = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    if re.match(ip_regex, ipv4address):
        return True
    else:
        return False

def ip_to_geo(ipaddress):
    """Convert IP to Geographic Information"""

    geo = gi.record_by_addr(ipaddress)

    return geo

def domain_to_geo(domain):
    """Convert Domain to Geographic Information"""

    geo = gi.record_by_name(domain)

    return geo

def ip_to_geojson(ipaddress, name="Point"):
    """Generate GeoJSON for given IP address"""

    geo = gi.record_by_addr(ipaddress)

    point = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": name
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        geo["longitude"],
                        geo["latitude"]
                    ]
                }
            }
        ]
    }

    return point

def ips_to_geojson(ipaddresses):
    """Generate GeoJSON for given IP address"""

    features = []

    for ipaddress in ipaddresses:
        geo = gi.record_by_addr(ipaddress)

        features.append({
            "type": "Feature",
            "properties": {
                "name": ipaddress
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    geo["longitude"],
                    geo["latitude"]
                ]
            }
        })

    points = {
        "type": "FeatureCollection",
        "features": features
    }

    return points

def reverse_dns_sna(ipaddress):
    """Returns a list of the dns names that point to a given ipaddress using StatDNS API"""

    r = requests.get("http://api.statdns.com/x/%s" % ipaddress)

    if r.status_code == 200:
        names = []

        for item in r.json()['answer']:
            name = str(item['rdata']).strip(".")
            names.append(name)

        return names
    else:
        raise Exception("No PTR record for %s" % ipaddress)
        return ""

def reverse_dns(ipaddress):
    """Returns a list of the dns names that point to a given ipaddress"""

    name, alias, addresslist = socket.gethostbyaddr(ipaddress)
    return [str(name)]
