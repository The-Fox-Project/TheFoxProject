import subprocess

from _internal.nmap.parser import NmapParser


# class to interact with the nmap command line interface
class NmapCli:

    def __init__(self):
        self.scan = None

    # run nmap with the given arguments
    def scan_ip(self, ip, *args):
        pipe = subprocess.Popen(["nmap", *args, ip, "-oX", "-"], stdout=subprocess.PIPE)

        # get the output
        res = pipe.communicate()[0]

        # parse the output
        self.scan = NmapParser(res).scan

        return self.scan


