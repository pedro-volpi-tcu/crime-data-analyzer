from typing import TypedDict


class ExpenseResponse(TypedDict):
    ano: int
    orgao: str
    codigoOrgao: str
    orgaoSuperior: str
    codigoOrgaoSuperior: str
    empenhado: str
    liquidado: str
    pago: str
