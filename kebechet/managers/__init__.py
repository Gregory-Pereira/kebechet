"""Managers implemented in Kebechet."""

from .info import InfoManager
from .update import UpdateManager
from .version import VersionManager  # noqa F401
from .pipfile_requirements import PipfileRequirementsManager
from .thoth_advise import ThothAdviseManager
from .thoth_provenance import ThothProvenanceManager
from .label_bot import ThothLabelBotManager
from .config_initializer import ConfigInitializer  # noqa F401
from .manager import ManagerBase  # noqa F401
from .manager import ManagerFailedException  # noqa F401

REGISTERED_MANAGERS = {
    "update": UpdateManager,
    "info": InfoManager,
    "version": VersionManager,
    "pipfile-requirements": PipfileRequirementsManager,
    "label-bot": ThothLabelBotManager,
    "thoth-advise": ThothAdviseManager,
    "thoth-provenance": ThothProvenanceManager,
}
