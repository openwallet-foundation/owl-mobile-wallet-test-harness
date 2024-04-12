import asyncio
import json
from time import sleep
from typing import Tuple

from aiohttp import (ClientError, ClientRequest, ClientResponse, ClientSession,
                     ClientTimeout, web)

######################################################################
# coroutine utilities
######################################################################


def run_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine())
    finally:
        loop.close()


def run_coroutine_with_args(coroutine, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine(*args))
    finally:
        loop.close()


def run_coroutine_with_kwargs(coroutine, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine(*args, **kwargs))
    finally:
        loop.close()


async def make_agent_controller_request(
    method, path, data=None, text=False, params=None
) -> (int, str):
    params = {k: v for (k, v) in (params or {}).items() if v is not None}
    client_session: ClientSession = ClientSession()
    async with client_session.request(method, path, json=data, params=params) as resp:
        resp_status = resp.status
        resp_text = await resp.text()
        await client_session.close()
        return (resp_status, resp_text)


def agent_controller_GET(url, topic, operation=None, id=None) -> Tuple[int, str]:
    agent_url = url + topic
    if operation:
        agent_url = agent_url + "/" + operation
    if id:
        agent_url = agent_url + "/" + id
    (resp_status, resp_text) = run_coroutine_with_kwargs(
        make_agent_controller_request, "GET", agent_url
    )
    return (resp_status, resp_text)


def agent_controller_POST(
    url, topic, operation=None, id=None, data=None, wrap_data_with_data=True
) -> Tuple[int, str]:
    agent_url = url + topic + "/"
    print(agent_url)
    payload = {}
    if data:
        if wrap_data_with_data:
            payload["data"] = data
        else:
            payload = data
    if operation:
        agent_url = agent_url + operation
    if id:
        if topic == "credential":
            payload["cred_ex_id"] = id
        else:
            payload["id"] = id

    (resp_status, resp_text) = run_coroutine_with_kwargs(
        make_agent_controller_request, "POST", agent_url, data=payload
    )
    return (resp_status, resp_text)


def agent_controller_DELETE(url, topic, id=None, data=None) -> (int, str):
    agent_url = url + topic + "/"
    if id:
        agent_url = agent_url + id
    (resp_status, resp_text) = run_coroutine_with_kwargs(
        make_agent_controller_request, "DELETE", agent_url
    )
    return (resp_status, resp_text)


def expected_agent_state(
    agent_url, protocol_txt, thread_id, status_txt, wait_time=2.0, sleep_time=0.5
) -> bool:
    sleep(sleep_time)
    state = "None"
    if type(status_txt) != list:
        status_txt = [status_txt]
    # "N/A" means that the controller can't determine the state - we'll treat this as a successful response
    status_txt.append("N/A")
    # for i in range(int(wait_time/sleep_time)):
    for i in range(int(wait_time)):
        (resp_status, resp_text) = agent_controller_GET(
            agent_url, protocol_txt, id=thread_id
        )
        if resp_status == 200:
            resp_json = json.loads(resp_text)
            state = resp_json["state"]
            rfc23_state = resp_json["rfc23_state"]
            if state in status_txt or rfc23_state in status_txt:
                return True
        sleep(sleep_time)
    return False


def expected_agent_proof_state(
    agent_url, thread_id, status_txt, wait_time=2.0, sleep_time=0.5
):
    sleep(sleep_time)
    verified = "False"
    if type(status_txt) != list:
        status_txt = [status_txt]
    for i in range(int(wait_time)):
        (resp_status, resp_text) = agent_controller_GET(
            agent_url + "/agent/command/", "proof", id=thread_id
        )
        if resp_status == 200:
            resp_json = json.loads(resp_text)
            # if "verified" is not in resp_json, then it hasn't been verified yet, loop.
            if "verified" in resp_json:
                verified = resp_json["verified"]
                if verified in status_txt:
                    return True
            else:
                print(
                    "Proof not verified on attempt",
                    i,
                    "of",
                    int(wait_time),
                    "sleeping for",
                    sleep_time,
                    "seconds",
                )
                # print formated json
                print(json.dumps(resp_json, indent=4))
        sleep(sleep_time)

    print(
        "From",
        agent_url,
        "Expected state",
        status_txt,
        "but received",
        verified,
        ", with a response status of",
        resp_status,
    )
    return False


def check_if_already_connected(context, sender, receiver):
    # get receiver DID

    receiver_url = context.config.userdata.get(receiver)
    (resp_status, resp_text) = agent_controller_GET(
        receiver_url + "/agent/command/", "did"
    )

    if resp_status == 200:
        resp_json = json.loads(resp_text)
        # assign thier_did
        receiver_did = resp_json["did"]

        # call GET connections for the sender with the receivers DID
        sender_url = context.config.userdata.get(sender)
        (sender_resp_status, sender_resp_text) = agent_controller_GET(
            sender_url + "/agent/command/", "active-connection", id=receiver_did
        )
        if sender_resp_status == 200:
            sender_resp_json = json.loads(sender_resp_text)
            sender_connection_id = sender_resp_json["connection_id"]
            sender_did = sender_resp_json["my_did"]

            # call GET connections for the receiver with the senders did
            (resp_status, resp_text) = agent_controller_GET(
                receiver_url + "/agent/command/", "active-connection", id=sender_did
            )
            if resp_status == 200:
                resp_json = json.loads(resp_text)
                receiver_connection_id = resp_json["connection_id"]

                # Populate connection id dictionary in context
                if not hasattr(context, "connection_id_dict"):
                    context.connection_id_dict = {}
                    context.connection_id_dict[sender] = {}
                    context.connection_id_dict[receiver] = {}

                context.connection_id_dict[sender][receiver] = sender_connection_id
                context.connection_id_dict[receiver][sender] = receiver_connection_id

                return True
            else:
                raise Exception(
                    f"Problem retreiving receiver's ({receiver}) connection id for active connection. Senders ({sender}) active connection info: {sender_resp_text}"
                )

    return False


def setup_already_connected(
    context, requester_connection_info_json, requester, responder
):
    requester_connection_id = requester_connection_info_json["connection_id"]
    requester_did = requester_connection_info_json["my_did"]
    responder_url = context.config.userdata.get(responder)

    # call GET connection for the responder with the requester did
    (resp_status, resp_text) = agent_controller_GET(
        responder_url + "/agent/command/", "active-connection", id=requester_did
    )
    if resp_status == 200:
        resp_json = json.loads(resp_text)
        responder_connection_id = resp_json["connection_id"]

        # Populate connection id dictionary in context
        if not hasattr(context, "connection_id_dict"):
            context.connection_id_dict = {}

        if requester not in context.connection_id_dict:
            context.connection_id_dict[requester] = {}
        if responder not in context.connection_id_dict:
            context.connection_id_dict[responder] = {}

        context.connection_id_dict[requester][responder] = requester_connection_id
        context.connection_id_dict[responder][requester] = responder_connection_id

        return True
    else:
        raise Exception(
            f"Problem retreiving responder's ({responder}) connection id for active connection. Requester's ({requester}) active connection info: {resp_text}"
        )
