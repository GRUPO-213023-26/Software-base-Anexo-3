
import logging

# Configuracion basica del logger.
# Todo se guarda en el archivo logs.txt, con fecha y hora.
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Guarda un evento normal del sistema (algo que salio bien)."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error del sistema (algo que fallo)."""
    logger.error(mensaje)
