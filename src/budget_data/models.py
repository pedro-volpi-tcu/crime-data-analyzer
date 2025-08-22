from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExpenseResponse:
    """Representa as dotações orçamentárias retornadas pela API do Portal da Transparência."""

    ano: int
    orgao: str
    codigo_orgao: str
    orgao_superior: str
    codigo_orgao_superior: str
    empenhado: Decimal
    liquidado: Decimal
    pago: Decimal

    @classmethod
    def from_api_dict(cls, data: dict[str, str]) -> "ExpenseResponse":
        """Factory method to create ExpenseResponse from API response dictionary."""
        return cls(
            ano=int(data["ano"]),
            orgao=data["orgao"],
            codigo_orgao=data["codigoOrgao"],
            orgao_superior=data["orgaoSuperior"],
            codigo_orgao_superior=data["codigoOrgaoSuperior"],
            empenhado=cls._parse_currency(data["empenhado"]),
            liquidado=cls._parse_currency(data["liquidado"]),
            pago=cls._parse_currency(data["pago"]),
        )

    @staticmethod
    def _parse_currency(value: str) -> Decimal:
        """Parse BRL to Decimal."""
        cleaned = value.replace(".", "").replace(",", ".")
        return Decimal(cleaned).quantize(Decimal("0.01"))
