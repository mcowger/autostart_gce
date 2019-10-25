import base64
import googleapiclient.discovery
from pprint import pprint
import json
from py_pushover_simple import pushover

compute = googleapiclient.discovery.build('compute', 'v1')


def send_message(message, user, token):
    p = pushover.Pushover()
    p.user = user
    p.token = token
    p.sendMessage(message)


def start(project="mcowger", zone="us-central1-a", instance=None):
    try:
        result = compute.instances().start(
            project=project, zone=zone, instance=instance).execute()
    except Exception:
        pass



def stop(project="mcowger", zone="us-central1-a", instance=None):
    try:
        result = compute.instances().stop(
            project=project, zone=zone, instance=instance).execute()
    except Exception:
        pass



def startstop(event, context):
    print("""This Function was triggered by messageId {} published at {}""".format(
        context.event_id, context.timestamp))
    input = json.loads(
        base64.decodestring(
            bytes(
                event['data'],
                "utf-8"
            )
        )
    )
    if (input['command'] == 'start'):
        start(
            project=input['project'],
            zone=input['zone'],
            instance=input['instance']
        )

    if (input['command'] == 'stop'):
        stop(
            project=input['project'],
            zone=input['zone'],
            instance=input['instance']
        )
    send_message(
        "command {} received for instance {}".format(
            input['command'], input['instance']),
        input['pushover_api']['user_key'],
        input['pushover_api']['app_token']
    )
