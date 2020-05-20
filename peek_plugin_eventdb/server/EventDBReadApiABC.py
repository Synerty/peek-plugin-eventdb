from abc import ABCMeta, abstractmethod
from typing import Optional, List

from rx.subjects import Subject
from twisted.internet.defer import Deferred


class EventDBReadApiABC(metaclass=ABCMeta):
    @abstractmethod
    def priorityKeysObservable(self, modelSetName: str) -> Subject:
        """ Priority Event DB Key Observable

        This observable emits list of keys that the EventDB acquisition plugins should
        prioritised, these keys will be monitored until the next
        priorityEventDBKey update.

        This list will represent keys relating to the objects that are
        currently being viewed.

        :param modelSetName:  The name of the model set of the keys to observe.

        :return: An observable that emits a List[str].

        """

    @abstractmethod
    def pollKeysObservable(self, modelSetName: str) -> Subject:
        """ Poll Event DB Key Observable

        This observable emits list of keys that the EventDB acquisition plugins should
        poll ONCE.

        This list will represent keys relating to the objects that are
        currently being viewed.

        :param modelSetName:  The name of the model set of the keys to observe.

        :return: An observable that emits a List[str].

        """

    @abstractmethod
    def itemAdditionsObservable(self, modelSetName: str) -> Subject:
        """ Event DB Tuple Added Items Observable

        Return an observable that fires when eventdb items are added

        :param modelSetName: The name of the model set for the EventDB

        :return: An observable that fires when keys are removed from the EventDB
        :rtype: An observable that emits List[EventDBDisplayValueTuple]

        """

    @abstractmethod
    def itemDeletionsObservable(self, modelSetName: str) -> Subject:
        """ Event DB Tuple Removed Items Observable

        Return an observable that fires when eventdb items are removed

        :param modelSetName:  The name of the model set for the EventDB

        :return: An observable that fires when keys are removed from the EventDB
        :rtype: An observable that emits List[str]

        """

    @abstractmethod
    def bulkLoadDeferredGenerator(self, modelSetName: str,
                                  keyList: Optional[List[str]] = None,
                                  chunkSize: int = 2500) -> Deferred:
        """ Event DB Tuples

        Return a generator that returns deferreds that are fired with chunks of the
         entire EventDB.

        :param chunkSize: The number of items to return for each chunk
        :param modelSetName:  The name of the model set for the EventDB
        :param keyList:  An optional list of keys that the data is required for

        :return: A deferred that fires with a list of tuples
        :rtype: C{EventDBDisplayValueTuple}

        This is served up in chunks to prevent ballooning the memory usage.

        Here is an example of how to use this method

        ::

                @inlineCallbacks
                def loadFromDiagramApi(diagramEventDBApi:DiagramEventDBApiABC):
                    deferredGenerator = diagramEventDBApi.bulkLoadDeferredGenerator("modelName")

                    while True:
                        d = next(deferredGenerator)
                        eventdbValueTuples = yield d # List[EventDBDisplayValueTuple]

                        # The end of the list is marked my an empty result
                        if not eventdbValueTuples:
                            break

                        # TODO, do something with this chunk of eventdbValueTuples



        """

    @abstractmethod
    def rawValueUpdatesObservable(self, modelSetName: str) -> Subject:
        """ Raw Value Update Observable

        Return an observable that fires with lists of C{EventDBRawValueTuple} tuples
        containing updates to EventDB values.

        :param modelSetName:  The name of the model set for the EventDB

        :return: An observable that fires when values are updated in the eventdb
        :rtype: Subject[List[EventDBRawValueTuple]]

        """

    @abstractmethod
    def displayValueUpdatesObservable(self, modelSetName: str) -> Subject:
        """ Display Value Update Observable

        Return an observable that fires with lists of C{EventDBDisplayValueTuple} tuples
        containing updates to EventDB values.

        :param modelSetName:  The name of the model set for the EventDB

        :return: An observable that fires when values are updated in the eventdb
        :rtype: An observable that fires with List[EventDBDisplayValueTuple]

        """
