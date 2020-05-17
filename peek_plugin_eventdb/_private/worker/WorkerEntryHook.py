import logging

from peek_plugin_base.worker.PluginWorkerEntryHookABC import PluginWorkerEntryHookABC
from peek_plugin_eventdb._private.storage.DeclarativeBase import loadStorageTuples
from peek_plugin_eventdb._private.tuples import loadPrivateTuples
from peek_plugin_eventdb._private.worker.tasks import EventDBItemImportTask, \
    EventDBItemUpdateTask, BulkLoadChunkTask
from peek_plugin_eventdb.tuples import loadPublicTuples

logger = logging.getLogger(__name__)


class WorkerEntryHook(PluginWorkerEntryHookABC):
    def load(self):
        loadStorageTuples()
        loadPrivateTuples()
        loadPublicTuples()

        logger.debug("loaded")

    def start(self):
        logger.debug("started")

    def stop(self):
        logger.debug("stopped")

    def unload(self):
        logger.debug("unloaded")

    @property
    def celeryAppIncludes(self):
        return [EventDBItemImportTask.__name__,
                EventDBItemUpdateTask.__name__,
                BulkLoadChunkTask.__name__]

