import argparse
import logging, csv, uuid

from app.db.db_util import create_user
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating user")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputcsv")
    args = vars(parser.parse_args())
    input_csv = args['inputcsv']
    db = SessionLocal()
    if input_csv:
        with open(input_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                created, user = create_user(db, fullname=row['name'], email=row['email'], password=row['password'], uuid=uuid.uuid4())
                print(f'created user: {user.email}' if created == True else f'user already exists: {user.email}')

if __name__ == "__main__":
    main()