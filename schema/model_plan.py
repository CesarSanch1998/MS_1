from pydantic import BaseModel
from typing import Optional
from typing import ClassVar

# ----------------------------------------------------------------------
# Clases para modificar usuario en DB y OLT
# ----------------------------------------------------------------------
class modify_client(BaseModel):
    """Datos necesarios para modificar el usuario en la db y olt  ."""
    contract : str
    frame : int
    slot : int
    port  : int
    onu_id : int
    olt : int
    name_1 :  str
    name_2 : str
    sn : str
    device :  str
    plan_name_old : str
    plan_name_new : str
    
class first_structure_modify(BaseModel):
    """Estructura superior de la consulta ."""
    api_key:str
    data:modify_client

# ----------------------------------------------------------------------
# Clases para modificar en todos los clientes  usuario en DB y OLT
# ----------------------------------------------------------------------
class modify_plan_all_client(BaseModel):
    """Datos necesarios para modificar el usuario en la db y olt  ."""
    contract : str
    frame : int
    slot : int
    port  : int
    onu_id : int
    name_1 :  str
    name_2 : str
    sn : str
    device :  str
    plan_name_old : str
    plan_name_new : str


class first_structure_modify_all(BaseModel):
    """Estructura superior de la consulta ."""
    api_key:str
    olt:int
    data: list[modify_plan_all_client]
