# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.vocab import Vocab  # noqa
from app.models.lemma import Lemma  # noqa
from app.models.definition import Definition  # noqa
from app.models.user import User  # noqa
