import nmap
import sys

sys.path.append("..")
from _internal.console import Logger
from rich import print
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.status import Status
from . import Modules

install()  # install rich traceback


class NmapModule(Modules):
    nm = nmap.PortScanner()
    console = Console()

    def name(self):
        return "nmap"

    def __str__(self):
        return "Nmap Scan"

    def scan_ip(self, ip, arguments, port=None):
        scan = self.nm.scan(ip, port, sudo=True, arguments=arguments)
        return scan

    def init(self):
        pass

    def main(self, logger: Logger, **kwargs):
        logger.info("scanning ip")
        res = self.scan_ip(**kwargs)
        ip = kwargs["ip"]
        logger.success("scan completed")
        table = Table(title="Nmap Scan Results", show_header=True, header_style="bold magenta")
        table.add_column("Protocol", style="dim", width=12)
        table.add_column("Port", style="dim", width=12)
        table.add_column("State")
        table.add_column("Service")
        table.add_column("Version")
        for port in res["scan"][ip]["tcp"]:
            version = res["scan"][ip]["tcp"][port]["version"]
            if version == "":
                version = "unknown"
            table.add_row(
                "tcp",
                str(port),
                res["scan"][ip]["tcp"][port]["state"],
                res["scan"][ip]["tcp"][port]["name"],
                version,
            )
        self.console.print(table)

        return res