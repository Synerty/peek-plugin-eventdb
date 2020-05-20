import logging
from typing import List

from twisted.internet.defer import Deferred, inlineCallbacks

from peek_plugin_base.storage.RunPyInPg import runPyInPg
from peek_plugin_eventdb._private.server.EventDBReadApi import EventDBReadApi
from peek_plugin_eventdb._private.server.controller.EventDBImportInPgTask import \
    EventDBImportInPgTask

logger = logging.getLogger(__name__)


class EventDBImportController:
    """ EventDB Import Controller
    """

    def __init__(self, dbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    def setReadApi(self, readApi: EventDBReadApi):
        self._readApi = readApi

    def shutdown(self):
        self._readApi = None

    @inlineCallbacks
    def importEvents(self, modelSetKey: str,
                     eventsEncodedPayload: str) -> Deferred:
        yield runPyInPg(logger,
                        self._dbSessionCreator,
                        EventDBImportInPgTask.importEvents,
                        modelSetKey,
                        eventsEncodedPayload)

    @inlineCallbacks
    def deleteEvents(self, modelSetKey: str, eventKeys: List[str]) -> Deferred:
        yield runPyInPg(logger,
                        self._dbSessionCreator,
                        EventDBImportInPgTask.deleteEvents,
                        modelSetKey,
                        eventKeys)
