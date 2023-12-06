from rich.console import Console

from _internal.exploitdb import pretty_print_exploits, search_exploits
from . import Modules


class VulnerabilitiesModule(Modules):
    console = Console()

    def __init__(self, *modules):
        super().__init__(modules)

    def name(self):
        return "vulnerabilities"

    def __str__(self):
        return "Vulnerabilities Scan"

    def require(self):
        return ["nmap"]  # require nmap module

    def init(self):
        pass

    def search_vulnerabilities(self, scan, host):
        for port in scan["scan"][host]["tcp"]:
            version = scan["scan"][host]["tcp"][port]["version"]
            if version == "":
                version = "unknown"
            service = scan["scan"][host]["tcp"][port]["name"]
            exploit_str = "No exploit found"
            message = f"[bold italic] {service}[/ bold italic]({version})\n"
            if version != "unknown" and service != "unknown":
                exploits = search_exploits(service + " " + version)
                if len(exploits) > 0:
                    pretty_print_exploits(exploits, self.console)
                    exploit_str = f"Exploit found: \n"
                    for exploit in exploits:
                        exploit_str += f"- {exploit['description']}\n"
                    exploit_str += f"{len(exploits)} exploits found"
                    message += exploit_str
                else:
                    message += "No vulnerabilities found" + "\n"
                self.console.print(message)

    def main(self, logger, **kwargs):
        scan = kwargs["nmap"]

        logger.info("searching for vulnerabilities")
        for host in scan["scan"]:
            self.console.print(f"[bold blue] {host} [/bold blue]")
            self.search_vulnerabilities(scan, host)
        logger.success("vulnerabilities scan completed")
