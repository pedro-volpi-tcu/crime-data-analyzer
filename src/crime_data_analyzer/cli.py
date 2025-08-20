# coding=utf-8 models.py
import argparse
import logging
from . import config

logger = logging.getLogger(__name__)

def handle_cli_args():
    parser = argparse.ArgumentParser(
        description="Ferramenta para analisar dados de segurança pública."
    )
    parser.add_argument(
        "--clear",
        action="store_true", # Transforma o argumento em uma flag booleana
        help="Apaga o arquivo de dados serializado para forçar uma reconstrução a partir da fonte."
    )
    args = parser.parse_args()

    if args.clear:
        logger.info(f"Argumento --clear detectado. Tentando apagar '{config.SERIALIZE_FILEPATH}'...")
        try:
            if config.SERIALIZE_FILEPATH.exists():
                config.SERIALIZE_FILEPATH.unlink() # Apaga o arquivo
                logger.info("Arquivo serializado apagado com sucesso.")
            else:
                logger.info("Nenhum arquivo serializado para apagar.")
        except OSError as e:
            logger.error(f'Impossível apagar o arquivo: {e}')
