import os, json 

from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy
)
import base64 
import json

def main() -> None:
    account_name = os.environ["STORAGE_ACCOUNT"]
    queue_name = os.environ["QUEUE_NAME"]

    account_url = f"https://{account_name}.queue.core.windows.net"

    credential = DefaultAzureCredential()

    queue = QueueClient(
        account_url=account_url,
        queue_name=queue_name,
        credential=credential,
    )
    #queue._message_encode_policy = BinaryBase64EncodePolicy()
    #queue._message_decode_policy = BinaryBase64DecodePolicy()

    # Send a message
    for n in range(5): 

        config = {
            'simulation_name':"some_name",
            'sectors':[],
            'subzone':'WATA1',
            'model':'crm_id',
            'use_faults':True,
            'distance_filter': 500,
            "encoded64": True  
        }


        raw = json.dumps( config )
        encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")

        queue.send_message( encoded )

        #queue.send_message(
        #    queue._message_encode_policy.encode(
        #        msg_send.encode("utf-8")
        #    )
        #)

        #send_result = queue.send_message("This is a test")#msg_send)
        #print("Message sent.")
        #print(f"Message ID: {send_result.id}")


    # Receive one message
    #print()
    #messages = queue.receive_messages(messages_per_page=1)

    #received_any = False
    #for msg in messages:
    #    received_any = True
    #    #print(f"Received message: {msg.content}")
    #    print("received message")

    #    #config = json.loads( msg.content )

    #    #print( config, type(config))


    #    # Delete after processing
    #    queue.delete_message(msg)
    #    print("Message deleted.")
    #    break

    #if not received_any:
    #    print("No messages available.")


if __name__ == "__main__":
    main()