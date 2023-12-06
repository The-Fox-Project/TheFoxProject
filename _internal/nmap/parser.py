import datetime

import _internal.nmap.scan as scan
from bs4 import BeautifulSoup


# Class to parse nmap output
class NmapParser:

    def __init__(self, xml):
        self.xml = xml
        self.scan = None  # scan.Scan but None for now
        self.parse()

    def parse(self):
        parser = BeautifulSoup(self.xml, "xml")

        nmap_run = parser.find("nmaprun")

        # Get scan arguments
        arguments = nmap_run["args"]
        start_time = self.parse_date(nmap_run["start"])

        children = nmap_run.findChildren("scaninfo")
        scan_info = children[0]

        scan_type = scan_info["type"]
        scan_num_services = self.parse_range(scan_info["numservices"])
        scan_services = int(scan_info["services"])
        protocol = self.parse_protocol(scan_info["protocol"])

        hosts = []
        xml_hosts = nmap_run.findChildren("host")

        for xml_host in xml_hosts:
            start_time = self.parse_date(xml_host["starttime"])
            end_time = self.parse_date(xml_host["endtime"])
            host_address = xml_host.findChildren("address")[0]["addr"]
            host_address_type = self.parse_ip_type(xml_host.findChildren("address")[0]["addrtype"])
            host_name = \
                list(map(
                    xml_host.findChildren("hostnames")[0].findChildren("hostname"),
                    lambda x: x["name"]
                ))

            ports = []
            xml_ports = xml_host.findChildren("ports")[0].findChildren("port")

            for xml_port in xml_ports:
                port_protocol = protocol
                port_number = int(xml_port["portid"])
                port_state = xml_port.find("state")

                scripts = []
                xml_scripts = xml_port.findChildren("script")

                for xml_script in xml_scripts:
                    script_name = xml_script["id"]
                    if "output" in xml_script:
                        script_output = xml_script["output"]
                    else:
                        script_output = xml_script.find().text
                    scripts.append(scan.Script(script_name, script_output))

                ports.append(
                    scan.Port(port_protocol, port_number, port_state, port_service, port_version, scripts)
                )

            os = xml_host.findChildren("os")
            os_accuracy = None
            os_family = None

            if os is not None:
                os = os[0]
                os_accuracy = int(os["accuracy"])
                os_family = os.findChildren("osmatch")[0]["name"]

            hosts.append(
                scan.Host(
                    host_address,
                    host_address_type,
                    host_name,
                    ports,
                    os,
                    os_accuracy,
                    os_family,
                    start_time,
                    end_time
                )
            )

        scan_stats = nmap_run.findChildren("runstats")[0]
        scan_stats_finished = scan_stats.findChildren("finished")[0]
        time = self.parse_date(scan_stats_finished["time"])
        host_up = int(scan_stats.findChildren("hosts")[0]["up"])
        host_down = int(scan_stats.findChildren("hosts")[0]["down"])
        host_total = int(scan_stats.findChildren("hosts")[0]["total"])

        scan_version = nmap_run["version"]

        self.scan = scan.Scan(
            hosts,
            arguments,
            time,
            host_up,
            host_down,
            host_total,
            scan_version,
            start_time,
            scan_type,
            scan_num_services,
            scan_services
        )

    def parse_date(self, date):
        return datetime.datetime.fromtimestamp(int(date))

    def parse_protocol(self, protocol):
        if protocol == "tcp":
            return scan.TCP
        elif protocol == "udp":
            return scan.UDP
        elif protocol == "sctp":
            return scan.SCTP
        else:
            raise ValueError(f"Unknown protocol: {protocol}")

    def parse_ip_type(self, ip_type):
        if ip_type == "ipv4":
            return scan.IPV4
        elif ip_type == "ipv6":
            return scan.IPV6
        else:
            raise ValueError(f"Unknown ip type: {ip_type}")

    def parse_range(self, ranges):
        split = ranges.split("-")
        if len(split) == 2:
            return range(int(split[0]), int(split[1]) + 1)
        else:
            raise ValueError(f"Invalid range: {ranges}")
