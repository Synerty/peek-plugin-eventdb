import logging
from typing import List

from twisted.internet.defer import Deferred, inlineCallbacks
from vortex.Payload import Payload

from peek_plugin_eventdb._private.server.EventDBReadApi import EventDBReadApi
from peek_plugin_eventdb._private.worker.tasks.EventDBItemImportTask import \
    importEventDBItems
from peek_plugin_eventdb.tuples.ImportEventDBItemTuple import ImportEventDBItemTuple

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
    def importEventDBItems(self, modelSetKey: str,
                          newItems: List[ImportEventDBItemTuple]) -> Deferred:
        """ Import Live DB Items

        1) set the  coordSetId

        2) Drop all disps with matching importGroupHash

        :param modelSetKey: The name of the model set
        :param newItems: The items to add or update to the live db
        :return:
        """

        newKeys = yield importEventDBItems.delay(
            modelSetKey=modelSetKey,
            newItems=newItems
        )

        newTuples = []

        deferredGenerator = self._readApi.bulkLoadDeferredGenerator(
            modelSetKey, keyList=newKeys)
        while True:
            d = next(deferredGenerator)
            result = yield d  # List[EventDBDisplayValueTuple]

            # The end of the list is marked my an empty result
            if not result or not result.count:
                break

            payload = yield Payload().fromEncodedPayloadDefer(result.encodedPayload)

            newTuples += payload.tuples

        # If there are no tuples, do nothing
        if not newTuples:
            return

        # Notify the agent of the new keys.
        self._readApi.itemAdditionsObservable(modelSetKey).on_next(newTuples)
