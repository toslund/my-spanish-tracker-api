import argparse
import logging, csv, uuid

from app.db.db_util import create_user
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating user")
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name")
    parser.add_argument("-e", "--email")
    parser.add_argument("-p", "--password")
    args = vars(parser.parse_args())
    name = args['name']
    email = args['email']
    password = args['password']
    if name and email and password:
        db = SessionLocal()
        created, user = create_user(db, fullname=name, email=email, password=password, uuid=uuid.uuid4())
        print(f'created user: {user.email}' if created == True else f'user already exists: {user.email}')
    else:
        logger.info("inputs not properly supplied")
if __name__ == "__main__":
    main()