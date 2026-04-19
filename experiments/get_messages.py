import os, json 

from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient


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

    # Send a message
    for n in range(5): 

        config = {
            'simulation_name':"some_name",
            'sectors':[],
            'subzone':'WATA1',
            'model':'crm_id',
            'use_faults':True,
            'distance_filter': 500 
        }


        msg_send = json.dumps( config )

        send_result = queue.send_message(msg_send)
        print("Message sent.")
        print(f"Message ID: {send_result.id}")


    # Receive one message
    messages = queue.receive_messages(messages_per_page=1)

    received_any = False
    for msg in messages:
        received_any = True
        print(f"Received message: {msg.content}")


        config = json.loads( msg.content )

        print( config, type(config))


        # Delete after processing
        queue.delete_message(msg)
        print("Message deleted.")
        break

    if not received_any:
        print("No messages available.")


if __name__ == "__main__":
    main()