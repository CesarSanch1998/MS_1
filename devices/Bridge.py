# from utils.ssh import ssh
import time
from utils.snmp_funtion import SNMP_Master
from config.definitions import olt_devices,snmp_oid,PORT
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from utils.spid import calculate_spid
load_dotenv()


# -------------------------------------------------------------------------------------------------
# Desinstalar cliente
# -------------------------------------------------------------------------------------------------
def unistall_bridge(command,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data["slot"],data["port"],data["onu_id"])
    ##----------------------------------
    #agregar comandos para quitar los datos del equipo si no se puede seguir la instalacion
    command(f'undo service-port {spid["I"]}')
    command(f'interface gpon {data["frame"]} {data["slot"]}')
    command(f'ont delete {data["port"]} {data["onu_id"]}')
    return HTTPException(status_code=202, detail={f"Client Unistalled succefuly"})

# -------------------------------------------------------------------------------------------------
# Reinstalar cliente
# -------------------------------------------------------------------------------------------------
def reinstall_bridge(command,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data["slot"],data["port"],data["onu_id"])
    command(f'undo service-port {spid["I"]}')
    command(f'interface gpon {data["frame"]}/{data["slot"]}')
    command(f'ont delete {data["port"]} {data["onu_id"]}')
    time.sleep(1)
    command(f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}" ')
    command(f'ont optical-alarm-profile {data["port"]} {data["onu_id"]} profile-id 3')
    command(f'ont alarm-policy {data["port"]} {data["onu_id"]} policy-id 1')
    command(f'ont fec {data["port"]} {data["onu_id"]} use-profile-config')
    command(f'ont port native-vlan {data["port"]} {data["onu_id"]} eth 1 vlan {data["vlan"]} priority 0')
    command(f'ont port native-vlan {data["port"]} {data["onu_id"]} eth 2 vlan {data["vlan"]} priority 0')
    
    command(f'quit')
    command(f'service-port {spid["I"]} vlan {data["vlan"]} gpon {data["frame"]}/{data["slot"]}/{data["port"]} ont {data["onu_id"]} gemport {data["gem_port"]} multi-service user-vlan {data["vlan"]} tag-transform transparent inbound traffic-table index {data["plan_idx"]} outbound traffic-table index {data["plan_idx"]}')
    command(f'interface gpon {data["frame"]}/{data["slot"]}')
    print(f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "