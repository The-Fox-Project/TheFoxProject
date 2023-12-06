from modules import Modules, nmap_module, vulnerabilities_module
import rich

if __name__ == "__main__":
    print(open("assets/foxlogo.txt").read())
    rich.print("[bold] Enums is the best [/bold]")
    rich.print("[bold yellow] WARNING: [/bold yellow] This tool is for educational purposes only")
    rich.print("[bold yellow] WARNING: [/bold yellow] I am not responsible for any damage caused by this tool")
    rich.print("[bold yellow] WARNING: [/bold yellow] This tool can take a long time to run")
    rich.print("[bold blue] FoxScan [/bold blue] - [bold green] v1.0 [/bold green]")
    console = rich.console.Console()
    modules = Modules(nmap_module.NmapModule(), vulnerabilities_module.VulnerabilitiesModule())
    modules.run({
        "nmap": {
            "ip": "scanme.nmap.org",
            "arguments": "-sV -sC -p-"
        }
    })