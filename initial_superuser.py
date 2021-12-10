import logging, json
import dropbox

from app.db.db_util import init_superuser
from app.db.session import SessionLocal
from app.schemas import definition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    db = SessionLocal()
    init_superuser(db)


def main() -> None:
    logger.info("Creating initial super user")
    init()


if __name__ == "__main__":
    main()