import logging

from sqlmodel import Session, select

from app.core.database import engine

from sqlalchemy import Engine
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_retries = 60 * 5 # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_retries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine:Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create a session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e

def main() -> None:
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")

if __name__ == "__main__":
    main()