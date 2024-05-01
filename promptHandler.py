from openai import OpenAI 
client = OpenAI()
import time
import os
import openai

#  copy the file id and assistant id directly from the Assistants page UI
knowledgebase_vector_id = "vs_VnLJAWvqrAgSzZTEi2zLn2fp"
assistant_id = "asst_o1TS4PfjlUmj65NaZdA7ApC3"

def handlePrompt(request):
    thread_id = "thread_Z4F4uIVoVMGHmCspMZpussCh"
    # thread_id = getThreadId(request)
    print(thread_id)
    sendPrompt(request["prompt"], thread_id)
    initiateRun(thread_id)
    return retrieveResponse(thread_id)

def getThreadId(request):
    if hasattr(request, 'thread_id') and request["thread_id"]:
        return request["thread_id"]
    else:
        thread_id = client.beta.threads.create(
            messages=[
                {
                "role": "user",
                    "content": "Hello, I am DönerGPT. How can I help you today",
                # Attach the new file to the message.
                # "attachments": [
                #     { "vector_store_id": knowledgebase_vector_id,"tools": [{"type": "file_search"}] }
                # ],
                }
            ]
            ).id
        return thread_id

def sendPrompt(message, thread_id):
    client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

def initiateRun(thread_id):
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Polling the run status until it completes
        while run.status not in ["completed", "failed"]:
            time.sleep(1)  # Wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            print("Checking run status:", run.status)

        if run.status == "completed":
            # Process your completed run
            print("Run completed successfully!")
        else:
            print("Run failed:", run.status)
            print(run)
    except openai.Error as e:
        print("An API error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", str(e))


    
def retrieveResponse(thread_id):
    # Assuming the run has been completed, retrieve the messages
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    response = messages.data[0].content[0].text.value # the first response
    # for message in messages:
    #     print(message.content)  # This will print all messages, including the Assistant’s responses.

    return response
    # return {
    #     "response": response,
    #     "thread_id": thread_id
    # }



# req = {
#     "thread_id" : None, "prompt": "Hi, I am Sonam" 
# }
# handlePrompt(req)

