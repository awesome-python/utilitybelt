import sys, os
import unittest

sys.path.insert(0, os.path.dirname(".."))

import utilitybelt as ub

class TestUB(unittest.TestCase):

    def setUp(self):
        pass

    ## isA Tests
    def test_is_IPv4Address(self):
        self.assertIsInstance(ub.is_IPv4Address("8.8.4.4"), bool)
        self.assertTrue(ub.is_IPv4Address("8.8.4.4"))
        self.assertTrue(ub.is_IPv4Address("127.0.0.1"))
        self.assertFalse(ub.is_IPv4Address("8.8.4"))
        self.assertFalse(ub.is_IPv4Address("google.com"))

    ## Geolocation Tests
    def test_ip_to_geo(self):
        self.assertIsInstance(ub.ip_to_geo("192.30.252.130"), dict)
        self.assertEqual(ub.ip_to_geo("192.30.252.130")["city"], 'San Francisco')
        self.assertEqual(ub.ip_to_geo("192.30.252.130")["region"], 'California')
        self.assertEqual(ub.ip_to_geo("192.30.252.130")["country"], 'United States')

    def test_domain_to_geo(self):
        pass

    def test_ip_to_geojson(self):
        pass

    def test_ips_to_geojson(self):
        pass

    ## Reverse DNS Tests
    def test_reverse_dns(self):
        self.assertIsInstance(ub.reverse_dns("192.30.252.130"), list)
        self.assertEqual(ub.reverse_dns("192.30.252.130"), ['github.com'])
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), ['google.com'])
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), 'github.com')
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), [])

    def test_reverse_dns_sna(self):
        self.assertIsInstance(ub.reverse_dns("192.30.252.130"), list)
        self.assertEqual(ub.reverse_dns("192.30.252.130"), ['github.com'])
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), ['google.com'])
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), 'github.com')
        self.assertNotEqual(ub.reverse_dns("192.30.252.130"), [])

if __name__ == '__main__':
    unittest.main()
