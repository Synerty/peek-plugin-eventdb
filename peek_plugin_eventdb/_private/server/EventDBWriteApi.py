import logging
from typing import List

from twisted.internet import defer
from twisted.internet.defer import Deferred, inlineCallbacks

from peek_plugin_eventdb._private.server.EventDBReadApi import EventDBReadApi
from peek_plugin_eventdb._private.server.controller.EventDBController import \
    EventDBController
from peek_plugin_eventdb._private.server.controller.EventDBImportController import \
    EventDBImportController
from peek_plugin_eventdb._private.server.controller.EventDBValueUpdateQueueController import \
    EventDBValueUpdateQueueController
from peek_plugin_eventdb.server.EventDBWriteApiABC import EventDBWriteApiABC
from peek_plugin_eventdb.tuples.ImportEventDBItemTuple import ImportEventDBItemTuple
from peek_plugin_eventdb.tuples.EventDBRawValueUpdateTuple import EventDBRawValueUpdateTuple

logger = logging.getLogger(__name__)


class EventDBWriteApi(EventDBWriteApiABC):

    def __init__(self):
        self._queueController = None
        self._eventdbController = None
        self._eventdbImportController = None
        self._readApi = None
        self._dbSessionCreator = None
        self._dbEngine = None

    def setup(self, queueController: EventDBValueUpdateQueueController,
              eventdbController: EventDBController,
              eventdbImportController: EventDBImportController,
              readApi: EventDBReadApi,
              dbSessionCreator,
              dbEngine):
        self._queueController = queueController
        self._eventdbController = eventdbController
        self._eventdbImportController = eventdbImportController
        self._readApi = readApi
        self._dbSessionCreator = dbSessionCreator
        self._dbEngine = dbEngine

    def shutdown(self):
        pass

    @inlineCallbacks
    def updateRawValues(self, modelSetName: str,
                        updates: List[EventDBRawValueUpdateTuple]) -> Deferred:
        """ Update Raw Values

        """
        if not updates:
            return

        yield self._queueController.queueData(modelSetName, updates)

        self._readApi.rawValueUpdatesObservable(modelSetName).on_next(updates)

    def importEventDBItems(self, modelSetName: str,
                          newItems: List[ImportEventDBItemTuple]) -> Deferred:
        if not newItems:
            return defer.succeed(True)

        return self._eventdbImportController.importEventDBItems(modelSetName, newItems)

    def prioritiseEventDBValueAcquisition(self, modelSetName: str,
                                         eventdbKeys: List[str]) -> Deferred:
        self._readApi.priorityKeysObservable(modelSetName).on_next(eventdbKeys)
        return defer.succeed(True)

    def pollEventDBValueAcquisition(self, modelSetName: str,
                                   eventdbKeys: List[str]) -> Deferred:
        self._readApi.pollKeysObservable(modelSetName).on_next(eventdbKeys)
        return defer.succeed(True)
