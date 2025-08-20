import logging

from . import config
from .builder import CrimeDataBuilder
from .models import CrimeData
from .serializer import CrimeDataSerializer

logger = logging.getLogger(__name__)


def load_or_build_data() -> CrimeData:
    logger.info("--- Iniciando carregamento de dados de Política Criminal ---")

    if not config.SERIALIZE_FILEPATH.exists():
        logger.info("Arquivo processado não encontrado. Construindo dados a partir da fonte...")
        builder = CrimeDataBuilder(config.INPUT_DIR)
        crime_data = builder.build()

        logger.info(f"Salvando dados processados para uso futuro em '{config.SERIALIZE_FILEPATH}'...")
        CrimeDataSerializer.serialize(crime_data, config.SERIALIZE_FILEPATH)

        return crime_data

    logger.info(f"Arquivo processado encontrado em '{config.SERIALIZE_FILEPATH}'. Carregando...")
    return CrimeDataSerializer.deserialize(config.SERIALIZE_FILEPATH)
