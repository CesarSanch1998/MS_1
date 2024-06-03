from db.connection import session,conn
from models.client import client_db
from models.plans import plans_db
from config.definitions import bridges,router,bdcm,snmp_oid,map_ports
from utils.ssh import ssh
from config.definitions import olt_devices
from devices.Router import reinstall_router
from devices.Bridge import reinstall_bridge
from devices.BDCM import reinstall_BDCM
from dotenv import load_dotenv
from utils.snmp_funtion import SNMP_Master
import os


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
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    print(clients_to_init_modify)
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
                            return clave
                        return None  
                    SNMP_Master("get",COMUNNITY, olt_devices[str(olt)], snmp_oid['equipment_id_register'],161,"equi_id",fsp_inicial=map_ports[],ont_id=users.onu_id)
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
                        "plan_name_old": users.plan_name_old,
                        "plan_name_new": returned.plan_name,
                        "plan_idx":returned.plan_idx,
                        "srv_profile":returned.srv_profile,
                        "vlan":returned.vlan,
                        "line_profile":returned.line_profile,
                        "gem_port":returned.gem_port,
                })
                    reinstall_BDCM(command,clients_to_init_modify)
    # print(data)
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()
        
    
    return data