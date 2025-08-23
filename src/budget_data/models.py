import abc
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Self


def parse_brazilian_decimal(value: str) -> Decimal:
    """Converts a Brazilian-style number string to a Decimal."""
    try:
        return Decimal(value.replace(".", "").replace(",", "."))
    except (InvalidOperation, AttributeError):
        return Decimal("0.0")


@dataclass
class BaseExpense(abc.ABC):
    """
    An abstract base class for all expense types.
    Represents the core data common to all responses.
    """

    ano: int
    empenhado: Decimal
    liquidado: Decimal
    pago: Decimal

    @staticmethod
    def _parse_common_fields(data: dict[str, str]) -> dict[str, int | Decimal]:
        return {
            "ano": int(data["ano"]),
            "empenhado": parse_brazilian_decimal(data["empenhado"]),
            "liquidado": parse_brazilian_decimal(data["liquidado"]),
            "pago": parse_brazilian_decimal(data["pago"]),
        }

    @classmethod
    @abc.abstractmethod
    def from_api_dict(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError


@dataclass
class OrganizationalExpense(BaseExpense):
    """Represents expenses grouped by organizational unit."""

    orgao: str
    codigo_orgao: str
    orgao_superior: str
    codigo_orgao_superior: str

    @classmethod
    def from_api_dict(cls, data: dict[str, str]) -> Self:
        common_fields = cls._parse_common_fields(data)

        specific_fields = {
            "orgao": data["orgao"],
            "codigo_orgao": data["codigo_orgao"],
            "orgao_superior": data["orgao_superior"],
            "codigo_orgao_superior": data["codigo_orgao_superior"],
        }

        return cls(**common_fields, **specific_fields)


@dataclass
class ProgrammaticExpense(BaseExpense):
    """Represents expenses grouped by programmatic function."""

    funcao: str | None
    codigo_funcao: str | None
    subfuncao: str | None
    codigo_subfuncao: str | None
    programa: str | None
    codigo_programa: str | None
    acao: str | None
    codigo_acao: str | None

    @classmethod
    def from_api_dict(cls, data: dict[str, str]) -> Self:
        common_fields = cls._parse_common_fields(data)

        specific_fields = {
            "funcao": data["funcao"],
            "codigo_funcao": data["codigoFuncao"],  # Map from JSON's camelCase
            "subfuncao": data["subfuncao"],
            "codigo_subfuncao": data["codigoSubfuncao"],
            "programa": data["programa"],
            "codigo_programa": data["codigoPrograma"],
            "acao": data["acao"],
            "codigo_acao": data["codigoAcao"],
        }

        return cls(**common_fields, **specific_fields)
