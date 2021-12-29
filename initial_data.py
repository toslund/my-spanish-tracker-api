import logging, json, sys
import dropbox

from app.core.config import settings
from app.db.db_util import populate_seed_data_objects
from app.db.session import SessionLocal
from app.schemas import definition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_data(dbx, file_path):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """

    md, res = dbx.files_download(file_path)

    data = res.content
    print(f'data type: {type(data)}')
    print(len(data), 'bytes; md:', md)

    # with io.BytesIO(res.content) as stream:
    #     txt = stream.read().decode()

    return json.loads(data)


def init(kw_dict) -> None:
    dbx = dropbox.Dropbox(settings.dropbox_token)
    db = SessionLocal()
    lemmas = retrieve_data(dbx, '/lemmas.json')
    vocabs = retrieve_data(dbx, '/vocabs.json')
    definitions = retrieve_data(dbx, '/definitions.json')
    users = retrieve_data(dbx, '/users.json')
    questions = retrieve_data(dbx, '/questions.json')
    decks = retrieve_data(dbx, '/decks.json')
    populate_seed_data_objects(
        db,
        lemmas=lemmas,
        vocabs=vocabs,
        definitions=definitions,
        users=users,
        questions=questions,
        decks=decks,
        over_ride_dates=kw_dict.get('over_ride_dates') == 'true'
    )


def main(kw_dict) -> None:
    logger.info("Creating initial data")
    init(kw_dict)
    logger.info("Initial data created")


if __name__ == "__main__":
    kw_dict = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            sep = arg.find('=')
            key, value = arg[:sep], arg[sep + 1:]
            kw_dict[key] = value

    main(kw_dict)

