import logging
from ..model.models import PathModel

logging.basicConfig(
    filename=PathModel.log_data,
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)
