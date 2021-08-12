# FRITZ!Box - UPNP Tool

This script uses UPnP to help you manage your FritzBox.  

| Option | Description | Value |
|----------|----------|----------|
| `--host` | Overwrite default "fritz.box" | IP or Hostname |
| `--port` | Overwrite default "49000" | Custom UPNP Port |
| `--renew` | Reconnect | None |
| `--getip` | Get connection status as XML | None |
| `--status` | Returns the public IP | None |
| `--debug` | Prints hostname, IP, port and response message | None |
&NewLine;

Example command line usage:

```sh
$ python3 main.py --getip --renew --getip --host 192.168.178.1
188.158.211.56
Reconnected
86.44.13.31
```

Example usage with cron:

```
30 04 * * * /usr/bin/python3 /root/main.py --renew --host 192.168.178.1
```