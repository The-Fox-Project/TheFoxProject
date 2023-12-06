import typing
import datetime

# State for port
CLOSE = 0
FILTERED = 1
OPEN = 2

# Ip type
IPV4 = 3
IPV6 = 4

# Different protocol
TCP = 5
UDP = 6
SCTP = 7


class Script(typing.NamedTuple):
    name: str
    output: str | None


class Port(typing.NamedTuple):
    protocol: TCP | UDP | SCTP
    port: int
    state: CLOSE | FILTERED | OPEN
    service: str
    version: str | None
    scripts: [Script]


class Host(typing.NamedTuple):
    ip: str
    ip_type: IPV4 | IPV6
    hostnames: [str]
    ports: [Port]
    os: str | None
    os_accuracy: int | None
    os_family: str | None
    start_time: datetime.datetime
    end_time: datetime.datetime


class Scan(typing.NamedTuple):
    hosts: [Host]
    arguments: str
    times: datetime.datetime
    host_up: int
    host_down: int
    host_total: int
    nmap_version: str
    started_at: datetime.datetime
    type: str
    service_scanned: range
    total_services: int
