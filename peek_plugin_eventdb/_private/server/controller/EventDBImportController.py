import logging
from datetime import datetime
from typing import List

import pytz
from twisted.internet.defer import Deferred, inlineCallbacks

from peek_plugin_base.storage.RunPyInPg import runPyInPg
from peek_plugin_eventdb._private.server.EventDBReadApi import EventDBReadApi
from peek_plugin_eventdb._private.server.controller.AdminStatusController import \
    AdminStatusController
from peek_plugin_eventdb._private.server.controller.EventDBImportInPgTask import \
    EventDBImportInPgTask

logger = logging.getLogger(__name__)


class EventDBImportController:
    """ EventDB Import Controller
    """

    def __init__(self, dbSessionCreator, statusController: AdminStatusController):
        self._dbSessionCreator = dbSessionCreator
        self._statusController = statusController

    def setReadApi(self, readApi: EventDBReadApi):
        self._readApi = readApi

    def shutdown(self):
        self._readApi = None

    @inlineCallbacks
    def importEvents(self, modelSetKey: str,
                     eventsEncodedPayload: str) -> Deferred:
        count = yield runPyInPg(logger,
                                self._dbSessionCreator,
                                EventDBImportInPgTask.importEvents,
                                modelSetKey,
                                eventsEncodedPayload)

        self._statusController.status.addedEvents += count
        self._statusController.status.lastActivity = datetime.now(pytz.utc)
        self._statusController.notify()

    @inlineCallbacks
    def deleteEvents(self, modelSetKey: str, eventKeys: List[str]) -> Deferred:
        count = yield runPyInPg(logger,
                                self._dbSessionCreator,
                                EventDBImportInPgTask.deleteEvents,
                                modelSetKey,
                                eventKeys)

        self._statusController.status.removedEvents += count
        self._statusController.status.lastActivity = datetime.now(pytz.utc)
        self._statusController.notify()
