import json, sys, os, io
from app.core.config import settings

from app.db.session import SessionLocal
from app.db.db_util import dump_data

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Uploads contents of file to Dropbox
def backup(local_file, dbx, backup_path):
    with open(local_file, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + local_file + " to Dropbox as " + backup_path + "...")
        try:
            dbx.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

# Uploads contents of file to Dropbox
def backup_f(data_dict, dbx, backup_path):
    # with open(local_file, 'rb') as f:
    # We use WriteMode=overwrite to make sure that the settings in the file
    # are changed on upload
    print("Uploading " + os.path.basename(backup_path) + " to Dropbox as " + backup_path + "...")
    try:
        with io.StringIO() as stream:
            json.dump(data_dict, stream, ensure_ascii=False) # Ident param is optional
            stream.seek(0)
            dbx.files_upload(stream.read().encode(), backup_path, mode=WriteMode('overwrite'))

        # dbx.files_upload(file_like, backup_path, mode=WriteMode('overwrite'))
    except ApiError as err:
        # This checks for the specific error where a user doesn't have
        # enough Dropbox space quota to upload this file
        if (err.error.is_path() and
                err.error.get_path().reason.is_insufficient_space()):
            sys.exit("ERROR: Cannot back up; insufficient space.")
        elif err.user_message_text:
            print(err.user_message_text)
            sys.exit()
        else:
            print(err)
            sys.exit()


def dump() -> None:
    dbx = dropbox.Dropbox(settings.dropbox_token)
    print(dbx.users_get_current_account())
    db = SessionLocal()
    lemmas, vocabs, definitions, users, questions, decks = dump_data(db)
    backup_f(lemmas, dbx, '/lemmas.json')
    backup_f(vocabs, dbx, '/vocabs.json')
    backup_f(definitions, dbx, '/definitions.json')
    backup_f(users, dbx, '/users.json')
    backup_f(questions, dbx, '/questions.json')
    backup_f(decks, dbx, '/decks.json')
    print('done')


def main() -> None:
    dump()


if __name__ == "__main__":
    main()
