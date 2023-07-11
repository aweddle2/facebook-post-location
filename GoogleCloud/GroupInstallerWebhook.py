import functions_framework
import json
from ..FacebookPostLocation.GroupInstaller import Install


@functions_framework.http
def process_post(request):
    request_args = request.args

    # Verify from the Facebook Developer Console
    verification_token = 'H74rtkX9UypM98kPn29Da5RdfD2UtMJwJU747uGGJV2zceHd3vAQnJXQ58GVT2XseGK5SAwG3ZQLvQHVCVvvdjUkDXAWpA6DRg4fBMTmcMPLXe7mLeBuz8WDHAsDcSJR'

    if request_args and 'hub.mode' in request_args and request_args['hub.mode'] == 'subscribe' and request_args['hub.verify_token'] == verification_token:
        return request_args['hub.challenge']

    # accept a payload from a group installing the app

    groupInstallRequest = FacebookGroupInstallRequest.from_json(
        json.loads(request.get_json(silent=True)))

    if (groupInstallRequest.value.verb == 'add'):
        Install('', groupInstallRequest.value.group_id)
    else:
        # TODO probably should support delete as a minimum
        raise ValueError('unsupported verb')

    return 'These are not the droids you are looking for!'


class FacebookGroupInstallRequest:
    def __init__(self, field, value):
        self.field = field
        self.value = FacebookGroupInstallValue.from_json(value)

    def __iter__(self):
        yield from {
            "field": self.field,
            "value": self.value
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return FacebookGroupInstallRequest(json_dct['field'], json_dct['value'])


class FacebookGroupInstallValue:
    def __init__(self, group_id, update_time, verb, actor_id):
        self.group_id = group_id
        self.update_time = update_time
        self.verb = verb
        self.actor_id = actor_id

    def __iter__(self):
        yield from {
            "group_id": self.group_id,
            "update_time": self.update_time,
            "verb": self.verb,
            "actor_id": self.actor_id,
        }.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.__str__()

    @staticmethod
    def from_json(json_dct):
        return FacebookGroupInstallValue(json_dct['group_id'], json_dct['update_time'], json_dct['verb'], json_dct['actor_id'])
