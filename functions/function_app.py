import logging
import json 
import azure.functions as func


#https://www.youtube.com/watch?v=swrzXmyTtrk

app = func.FunctionApp()

@app.queue_trigger(
    arg_name="msg",
    queue_name="queue-launcher-uksouth",
    connection="AzureWebJobsStorage"
)
def queue_trigger(msg:func.QueueMessage) -> None:
    #logging.info("\n\nFUNCTION ENTERED\n\n")
    # 1. Get raw bytes from queue
    #raw = msg.get_body()   # bytes
    config_as_str = msg.get_body().decode('utf-8') 

    #logging.info('Python queue trigger function processed a queue item: %s',config_as_str)

    config = json.loads( config_as_str )
    #logging.info('***Python object : %s',config)
    
    
    #x = base64.b64decode(raw)
    #logging.info(f"Decoded string: {raw}")
    
    # 2. Decode base64 → original bytes
    #decoded_bytes = base64.b64decode(raw)

    # 3. Convert to string
    #decoded_str = x.decode("utf-8")

    #logging.info(f"Decoded string: {decoded_str}")