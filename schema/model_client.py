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
    fsp : str
    fspi : str
    name_1 :  str
    name_2 : str
    status : str
    state : str
    sn : str
    device :  str
    plan_name : str
    spid : int

class first_structure_modify(BaseModel):
    """Estructura superior de la consulta ."""
    api_key:str
    data:modify_client
