from pysnmp.hlapi import *
from config.definitions import map_ports #,state_types
import binascii

from utils.failcheck import fail,check_power, check_sn,check_power_olt,check_equip_id
# from helpers.shows_progress import print_fsp

datos = {}

data = []
OPERATION = {
    "next":nextCmd,
    "get":getCmd,
    "bulk":bulkCmd,
}

# def null_datos():
#     datos.clear()
#     datos = {}
#     # print(datos)
                    
#-------------------REQUEST MASTER --------------------------------------
def SNMP_Master(op,community, host, oid,port,type_request,fsp_inicial="",ont_id=""):
    data.clear()
    iterator = OPERATION[op](
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid+f".{fsp_inicial}.{ont_id}")),
        lexicographicMode=False
    )
    # print(oid+f".{fsp_inicial}.{ont_id}")

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                ont_id = varBind[0].prettyPrint().split('.')[-1]
                resp = varBind[1].prettyPrint()


                if type_request=="equi_id":
                    equip_id_register =  resp
                    return equip_id_register
                
    return equip_id_register