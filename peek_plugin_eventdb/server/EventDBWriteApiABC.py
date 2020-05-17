from typing import List

from abc import ABCMeta, abstractmethod
from twisted.internet.defer import Deferred

from peek_plugin_eventdb.tuples.ImportEventDBItemTuple import ImportEventDBItemTuple
from peek_plugin_eventdb.tuples.EventDBDisplayValueUpdateTuple import \
    EventDBDisplayValueUpdateTuple
from peek_plugin_eventdb.tuples.EventDBRawValueUpdateTuple import EventDBRawValueUpdateTuple


class EventDBWriteApiABC(metaclass=ABCMeta):
    @abstractmethod
    def updateRawValues(self, modelSetName: str,
                        updates: List[EventDBRawValueUpdateTuple]) -> Deferred:
        """ Process Live DB Raw Value Updates

        Tells the live db that values have updated in the field, or wherever.

        :param modelSetName:  The name of the model set for the live db
        :param updates: A list of tuples containing the value updates

        :return: A deferred that fires when the update is complete.
        :rtype: bool

        """

    @abstractmethod
    def importEventDBItems(self, modelSetName: str,
                          newItems: List[ImportEventDBItemTuple]) -> Deferred:
        """ Import EventDB Items

        Create new Live DB Items with Raw + Display values

        If an item already exists, it's value is update.

        :param modelSetName:  The name of the model set for the live db
        :param newItems: A list of tuples containing the value updates

        :return: A deferred that fires when the inserts are complete.
        :rtype: bool

        """

    @abstractmethod
    def prioritiseEventDBValueAcquisition(self, modelSetName: str,
                                         eventdbKeys: List[str]) -> Deferred:
        """ Prioritise EventDB Value Acquisitions

        When this method was first created, it was used for the diagram to tell the
        RealTime agent which keys to update as they were viewed by the user.

        :param modelSetName:  The name of the model set for the live db
        :param eventdbKeys: A list of the eventdb keys to watch

        :return: A deferred that fires with True
        :rtype: bool

        """

    @abstractmethod
    def pollEventDBValueAcquisition(self, modelSetName: str,
                                         eventdbKeys: List[str]) -> Deferred:
        """ Poll EventDB Value Acquisitions

        Tell the EventDB plugin the eventdbKeys must be polled.

        This method should be called after a re-import of an existing grid.

        :param modelSetName:  The name of the model set for the live db
        :param eventdbKeys: A list of the eventdb keys to poll

        :return: A deferred that fires with True
        :rtype: bool

        """