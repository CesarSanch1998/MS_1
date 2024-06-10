# from utils.ssh import ssh
import time
from utils.snmp_funtion import SNMP_Master
from config.definitions import olt_devices,snmp_oid,PORT
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from utils.spid import calculate_spid
load_dotenv()

# Access environment variables
COMUNNITY = os.getenv("SNMP_READ")

# -------------------------------------------------------------------------------------------------
# Instalar cliente
# -------------------------------------------------------------------------------------------------
# def install_Router(command,ip,data):
#     # (comm, command, quit_ssh) = ssh(ip, True)
#     time.sleep(12)
#     # Agregar validacion automatica de potencia y temperatura
#     rx_ont = SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_ont"],PORT,"pw_ont",port_oid,data['onu_id'])
#     rx_olt= SNMP_Master("get",COMUNNITY,ip,snmp_oid["rx_olt"],PORT,"pw_olt",port_oid,data['onu_id'])

#     if rx_ont  <= -26.50 and rx_olt <= -31.50:

#         #agregar comandos para quitar los datos del equipo si no se puede seguir la instalacion
#         command(f"interface gpon {data['frame']} {data['slot']}")
#         command(f"ont delete {data['port']} {data['onu_id']}")
#         return HTTPException(status_code=202, detail={f"Equipo no instalado ont:{rx_ont}  y olt:{rx_olt}"})
    
#     spid = calculate_spid(data['slot'],data['port'],data['onu_id'])

#     command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['vlan']}")
#     command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 2")
#     command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")
#     command(f"quit")
#     command(f"service-port {spid["I"]} vlan {data['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {gem_port} multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index {plan_idx} outbound traffic-table index {plan_idx}")
#     command(f"interface gpon {data['frame']}/{data['slot']}")
#     command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
#     command(f"ont port route {data['port']} {data['onu_id']} eth 1-4 enable")

#     return {
#         "f/s/p/id":f"{data['frame']}/{data['slot']}/{data['port']}/{data['onu_id']}",
#         "nombre":{name},
#         "serial":{sn.upper()},
#         "vlan":{data['vlan']},
#         "spid":{spid["I"]},
#         "Equi_id":equipement_id,
#         "status":"OK"
#             }

# -------------------------------------------------------------------------------------------------
# Desinstalar cliente
# -------------------------------------------------------------------------------------------------
# def unistall_router(command,ip,data):
#     # (comm, command, quit_ssh) = ssh(ip, True)
#     ##----------------------------------
#     #agregar comandos para quitar los datos del equipo si no se puede seguir la instalacion
#     command(f"undo service-port {spid["I"]}")
#     command(f"interface gpon {data['frame']} {data['slot']}")
#     command(f"ont delete {data['port']} {data['onu_id']}")
#     return HTTPException(status_code=202, detail={f"Client Unistalled succefuly"})

# -------------------------------------------------------------------------------------------------
# Reinstalar cliente
# -------------------------------------------------------------------------------------------------
def reinstall_router(command,ip,data):
    # (comm, command, quit_ssh) = ssh(ip, True)
    spid = calculate_spid(data['slot'],data['port'],data['onu_id'])
    command(f"undo service-port {spid['I']}")
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont delete {data['port']} {data['onu_id']}")
    time.sleep(1)
    command(f'ont add {data["port"]} {data["onu_id"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]+" "+ data["name_2"] +" "+ data["contract"]}"')
    
    if data["state"] != 'active':
        command(f"ont deactivate {data['port']} {data['onu_id']}")
    
    command(f"ont optical-alarm-profile {data['port']} {data['onu_id']} profile-id 3")
    command(f"ont alarm-policy {data['port']} {data['onu_id']} policy-id 1")
    command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 1 dhcp vlan {data['vlan']} priority 0")
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 1")
    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 0")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0")
    command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")
    command(f"ont port route {data['port']} {data['onu_id']} eth 1-8 enable")
    command(f"quit")
    command(f"service-port {spid['I']} vlan {data['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data['gem_port']} multi-service user-vlan {data['vlan']} tag-transform transparent inbound traffic-table index {data['plan_idx']} outbound traffic-table index {data['plan_idx']}")
    print("\n")
    print(f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']}")
    return f"Plan reinstall Succefully in client {data['name_1']} {data['name_2']} {data['contract']} "
