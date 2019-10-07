#!/usr/bin/env pyhton3

import requests
import json
import warnings
import argparse

warnings.filterwarnings("ignore")


def check_supported_idrac_version(req):
    response = requests.get(f'https://{req["idrac_ip"]}/redfish/v1/Systems/'
                            'System.Embedded.1/Bios',
                            verify=False,
                            auth=(req["idrac_username"],
                                  req["idrac_password"]))
    if response.status_code != 200:
        return(False)
    else:
        return(True)


def get_bios_attributes(req):
    response = requests.get(f'https://{req["idrac_ip"]}/redfish/v1/Systems/'
                            'System.Embedded.1/Bios',
                            verify=False,
                            auth=(req['idrac_username'],
                                  req['idrac_password']))
    data = json.dumps(response.json()["Attributes"])
    return(data)


def get_specific_bios_attribute(req):
    response = requests.get(f'https://{req["idrac_ip"]}/redfish/v1/Systems/'
                            'System.Embedded.1/Bios',
                            verify=False,
                            auth=(req['idrac_username'],
                                  req['idrac_password']))
    data = response.json()['Attributes']
    new_value = {}
    new_value[req["idrac_attr"]] = data[req["idrac_attr"]]
    return(json.dumps(new_value))


def handle(req):
    parsed_req = json.loads(req)
    if check_supported_idrac_version(parsed_req):
        if 'idrac_attr' in parsed_req:
            print(get_specific_bios_attribute(parsed_req))
        else:
            print(get_bios_attributes(parsed_req))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Python script using Redfish "
                                     "API to get all BIOS attributes or get "
                                     "current value for one specific "
                                     "attribute")
    parser.add_argument('-ip', help='iDRAC IP address', required=True)
    parser.add_argument('-u', help='iDRAC username', required=True)
    parser.add_argument('-p', help='iDRAC password', required=True)
    parser.add_argument('-a', help="Pass in the attribute name you want to "
                        "get the current value, MemTest will work but memtest "
                        "will fail", required=False)
    idrac_args = {}
    args = vars(parser.parse_args())
    idrac_args['idrac_ip'] = args['ip']
    idrac_args['idrac_username'] = args['u']
    idrac_args['idrac_password'] = args['p']
    if args['a'] is not None:
        idrac_args['idrac_attr'] = args['a']
    handle(json.dumps(idrac_args))
