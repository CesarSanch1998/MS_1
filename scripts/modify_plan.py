from db.connection import session,conn
from models.client import client_db
from models.plans import plans_db
from config.definitions import bridges,router,bdcm,snmp_oid,map_ports,state_types
from utils.ssh import ssh
from config.definitions import olt_devices
from devices.Router import reinstall_router
from devices.Bridge import reinstall_bridge
from devices.BDCM import reinstall_BDCM
from dotenv import load_dotenv
from utils.snmp_funtion import SNMP_Master
import os
import json
import datetime


load_dotenv()

# Access environment variables
COMUNNITY = os.getenv("SNMP_READ")

clients_to_init_modify ={}

def modify_plan_client(data):
    (comm, command, quit_ssh) = ssh(olt_devices[str(data.olt)], True)

    try:
        returned = session.query(plans_db).filter(plans_db.plan_name == data.plan_name_new).first()
        if returned == None:
            return "Plan no existe en la DB"
        else:
            print(returned.plan_name)
        return data
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()

def modify_plan_all_client(olt,data):
    
    (comm, command, quit_ssh) = ssh(olt_devices[str(olt)], True)
    try:
        for users in data:
            returned = session.query(plans_db).filter(plans_db.plan_name == users.plan_name_new).first()
            if returned == None:
                return "Plan no existe en la DB"
            else:
                for clave, valor in map_ports.items():
                        if valor == f"{users.frame}/{users.slot}/{users.port}":
                            state_client = SNMP_Master("get",COMUNNITY, olt_devices[str(olt)], snmp_oid['state'],161,"state",fsp_inicial=clave,ont_id=users.onu_id)
                
                if users.device in bridges:
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    # print(clients_to_init_modify)
                    reinstall_bridge(command,clients_to_init_modify)
                    # print(f"{returned.plan_name} {returned.plan_idx} {returned.srv_profile} {returned.vlan} {returned.line_profile} {returned.gem_port}")
                elif users.device in router:
                    #ROUTER---------------------------
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                    # print(clients_to_init_modify)
                    # print(f"{returned.plan_name} {returned.plan_idx} {returned.srv_profile} {returned.vlan} {returned.line_profile} {returned.gem_port}")
                elif users.device in bdcm:
                    
                    for clave, valor in map_ports.items():
                        
                        if valor == f"{users.frame}/{users.slot}/{users.port}":
                            modelo_snmp = SNMP_Master("get",COMUNNITY, olt_devices[str(olt)], snmp_oid['equipment_id_register'],161,"equi_id",fsp_inicial=clave,ont_id=users.onu_id)
                            print(modelo_snmp)
                    
                    #BDCM---------------------------
                    clients_to_init_modify.update({})
                    clients_to_init_modify.update({
                        "contract": users.contract,
                        "frame": users.frame,
                        "slot": users.slot,
                        "port":users.port,
                        "onu_id":users.onu_id,
                        "name_1": users.name_1,
                        "name_2": users.name_2,
                        "sn": users.sn,
                        "state":state_types[state_client],
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    #Despues de saber si lo detecta como ONU-type-eth-4-pots-2-catv-0  lo verificamos con snmp para saber el equipo
                    if modelo_snmp == '1126':
                        reinstall_BDCM(command,clients_to_init_modify)
                    elif modelo_snmp in router:
                        reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                    elif modelo_snmp in router:
                        reinstall_bridge(command,clients_to_init_modify)
                    elif modelo_snmp == '':
                        print("EL EQUIPO ESTA APAGADO SE INSTALARA CONFIG PERSONALIZADA!!")
                        reinstall_router(command,olt_devices[str(olt)],clients_to_init_modify)
                        # fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d")
                        # with open(f"cliente_omitido-{fecha_hora}.json", "a") as archivo_json:
                        #     json.dump(clients_to_init_modify, archivo_json, indent=4)

    # print(data)
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()
        
    
    return data