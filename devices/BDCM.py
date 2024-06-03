import time
from config.definitions import olt_devices,snmp_oid,PORT
import os
from fastapi import HTTPException
from utils.spid import calculate_spid


# -------------------------------------------------------------------------------------------------
# Reinstalar cliente
# -------------------------------------------------------------------------------------------------
def reinstall_BDCM(command,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data['slot'],data['port'],data['onu_id'])
    command(f"undo service-port {spid['I']}")
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont delete {data['port']} {data['onu_id']}")
    time.sleep(1)
    command(f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}"')
    command(f"ont optical-alarm-profile {data['port']} {data['onu_id']} profile-id 3")
    command(f"ont alarm-policy {data['port']} {data['onu_id']} policy-id 1")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 1 dhcp vlan {data['vlan']} priority 0")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['vlan']} priority 5")
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 1")
    # command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")
    command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")
    # command(f"ont port route {data['port']} {data['onu_id']} eth 1-8 enable")
    command(f"quit")
    command(f"service-port {spid['I']} vlan {data['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data['gem_port']} multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index {data['plan_idx']} outbound traffic-table index {data['plan_idx']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "
