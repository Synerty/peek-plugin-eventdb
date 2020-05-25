from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

from peek_plugin_base.storage.DbConnection import DbSessionCreator
from peek_plugin_eventdb._private.PluginNames import eventdbFilt
from peek_plugin_eventdb._private.PluginNames import eventdbObservableName
from peek_plugin_eventdb._private.server.controller.AdminStatusController import \
    AdminStatusController
from peek_plugin_eventdb._private.server.tuple_providers.AdminStatusTupleProvider import \
    AdminStatusTupleProvider
from peek_plugin_eventdb._private.server.tuple_providers.EventDBModelSetTableTupleProvider import \
    EventDBModelSetTableTupleProvider
from peek_plugin_eventdb._private.storage.EventDBModelSetTable import EventDBModelSetTable
from peek_plugin_eventdb._private.tuples.AdminStatusTuple import \
    AdminStatusTuple


def makeTupleDataObservableHandler(ormSessionCreator: DbSessionCreator,
                                   adminStatusController: AdminStatusController):
    """" Make Tuple Data Observable Handler

    This method creates the observable object, registers the tuple providers and then
    returns it.

    :param adminStatusController:
    :param ormSessionCreator: A function that returns a SQLAlchemy session when called

    :return: An instance of :code:`TupleDataObservableHandler`

    """
    tupleObservable = TupleDataObservableHandler(
        observableName=eventdbObservableName,
        additionalFilt=eventdbFilt)

    # # Register TupleProviders here
    tupleObservable.addTupleProvider(AdminStatusTuple.tupleName(),
                                     AdminStatusTupleProvider(adminStatusController))

    tupleObservable.addTupleProvider(EventDBModelSetTable.tupleName(),
                                     EventDBModelSetTableTupleProvider(ormSessionCreator))
    return tupleObservable
