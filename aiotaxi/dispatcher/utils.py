from uuid import uuid4

from . import structs


def assign_dispatcher(status):
    dispatcher_id = str(uuid4())
    structs.dispatchers[dispatcher_id] = {
        'status': status
    }

    return dispatcher_id


def get_dispatcher(dispatcher_id):
    return structs.dispatchers[dispatcher_id]


def set_dispatcher_as_available(dispatcher_id):
    structs.available_dispatchers.append(dispatcher_id)
