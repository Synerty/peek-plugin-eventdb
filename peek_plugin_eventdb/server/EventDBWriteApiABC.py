from abc import ABCMeta, abstractmethod
from typing import List

from twisted.internet.defer import Deferred


class EventDBWriteApiABC(metaclass=ABCMeta):
    @abstractmethod
    def addEvents(self, modelSetName: str,
                  eventsEncodedPayload: str) -> Deferred:
        """ Add Events

        Tells the EventDB that values have updated in the field, or wherever.

        :param modelSetName:  The name of the model set for the EventDB
        :param eventsEncodedPayload: An encoded Payload containing a
         list of events to insert.

        :return: A deferred that fires when the insert is complete.
        :rtype: None

        """

    @abstractmethod
    def removeEvents(self, modelSetName: str, eventKeys: List[str]) -> Deferred:
        """ Add Item Events

        Tells the EventDB that values have updated in the field, or wherever.

        :param modelSetName:  The name of the model set for the EventDB
        :param eventKeys: An list of event keys to remove.

        :return: A deferred that fires when the removal is complete.
        :rtype: None

        """
