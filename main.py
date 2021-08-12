import urllib.request
from socket import gethostbyname_ex
from sys import argv
import xml.etree.ElementTree as ET
from time import sleep

def request(action, host="fritz.box", port=49000):
    soap_body = '\r\n'.join((
    '<?xml version="1.0" encoding="utf-8"?>',
    '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">',
    '  <s:Body>',
    '    <u:ForceTermination xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:2"/>',
    '  </s:Body>',
    '</s:Envelope>'))

    soap_action = "urn:schemas-upnp-org:service:WANIPConnection:2#" + action

    headers = {
        'SOAPAction': u'"%s"' % (soap_action),
        'Host': (host + ":" + str(port)),
        'Content-Type': 'text/xml',
        'Content-Length': len(soap_body),
    }

    ctrl_url = "http://" + host + ":" + str(port) + "/igd2upnp/control/WANIPConn1"

    request = urllib.request.Request(ctrl_url, bytes(soap_body, "utf-8"), headers)

    try:
        return urllib.request.urlopen(request).read().decode()
    except urllib.error.HTTPError as e:
        return e.read().decode()
    except urllib.error.URLError as e:
        return str(e)

def print_result(result, action, host, port, debug):
    if debug:
        print("Host:", host, "\nIP:", gethostbyname_ex(host)[2][0], "\nPort:", port, "\n")
        print(result)
    else:
        if "urlopen error" in result and ("getaddrinfo failed" in result or "Name or service not known" in result):
            print(f"Could not find", host, "\n")
            print(result)
            exit()
        elif ":service:WANIPConnection:2" in result:
            if "ForceTerminationResponse" in result:
                print("Reconnected")
            elif "GetStatusInfoResponse" in result:
                print(result)
            elif "GetExternalIPAddressResponse" in result:
                print(result[result.index("<NewExternalIPAddress>")+22:result.index("</NewExternalIPAddress>")])
        else:
            print("Host:", host, "\nIP:", gethostbyname_ex(host)[2][0], "\nPort:", port, "\n")
            print(result)

if __name__ == "__main__":

    # Process arguments
    if "--host" in argv[1:]:
        host = argv.pop(argv.index("--host")+1)
        argv.remove("--host")
    else:
        host = "fritz.box"

    if "--port" in argv[1:]:
        port = argv.pop(argv.index("--port")+1)
        argv.remove("--port")
    else:
        port = 49000

    if "--debug" in argv[1:]:
        debug = True
        argv.remove("--debug")
    else:
        debug = False

    actions = {
        "--renew": "ForceTermination",
        "--status": "GetStatusInfo",
        "--getip": "GetExternalIPAddress"
        }

    commands = [actions[i] for i in argv[1:] if i in actions.keys()]

    for i, action in enumerate(commands):
        # Wait until reconnected to request new IP
        if(action == "GetExternalIPAddress" and "ForceTermination" in commands[:i]):
            while("Connected" not in request("GetStatusInfo", host, port)):
                sleep(0.1)

        result = request(action, host, port)
        print_result(result, action, host, port, debug)