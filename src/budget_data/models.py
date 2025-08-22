from decimal import Decimal

from pydantic import Field, validator


class ExpenseResponse:
    """Representa as dotações orçamentárias retornadas pela API do Portal da Transparência."""

    ano: int
    orgao: str
    codigo_orgao: str = Field(alias="codigoOrgao")
    orgao_superior: str = Field(alias="orgaoSuperior")
    codigo_orgao_superior: str = Field(alias="codigoOrgaoSuperior")
    empenhado: Decimal
    liquidado: Decimal
    pago: Decimal

    @validator("empenhado", "liquidado", "pago", pre=True)
    def parse_currency(cls, value: str) -> Decimal:
        # Handle string format "1.310.051.787,40"
        cleaned = value.replace(".", "").replace(",", ".")
        return Decimal(cleaned).quantize(Decimal("0.01"))

    class Config:
        """Allows Pydantic to populate the model using the json field names."""

        allow_population_by_field_name = True
