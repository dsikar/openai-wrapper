import json
import os
import openai
from openai import OpenAI
import time

# helper functions

def show_json(obj):
    print(json.loads(obj.model_dump_json()))
    
def find_file_path(filename, location_hint):
    for root, dirs, files in os.walk(location_hint):
        if filename in files:
            return os.path.join(root, filename)
    return None

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input, assistant_id):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def get_assistant_response(assistant_id, assistant_query):
    """
    Get a response from the assistant
    Parameters
    ----------
    assistant_id : str
        The assistant id
    assistant_query : str
        The query to ask the assistant
    Returns
    -------
    assistant_reponse : str
        The assistant response
    Examples
    --------
    >>> assistant_id = "your-assistant-id"
    >>> assistant_query = "What is the capital of France?"
    >>> assistant_reply = get_assistant_response(assistant_id, assistant_query)
    >>> print(assistant_reply)
    Paris
    """
    thread, run = create_thread_and_run(
        assistant_query, assistant_id
    )
    run = wait_on_run(run, thread)
    assistant_response = get_response(thread)
    pretty_print(get_response(thread))
    return assistant_response

def create_assistant(filepath):
    file1 = client.files.create(
        file=open(filepath, "rb"),
        purpose='assistants'
    )
    assistant1 = client.beta.assistants.create(
        instructions="You are a literature review assistant. Use the paper to answer questions for example about the abstract, \
            main contributions and future work.",
        model="gpt-3.5-turbo-1106", # note original gpt-4-1106-preview not available
        tools=[{"type": "retrieval"}],
        file_ids=[file1.id]
    )
    return assistant1, file1.id

def delete_file_id(file_id):
    # does not seem to work
    client.files.delete(file_id)

def delete_all_file_ids():
    import re
    input_string = str(client.files.list())
    # SyncPage[FileObject](data=[FileObject(id='file-fDHXoZmZUxr2Zf4RrzTHf8yk', bytes=302962, created_at=1705864411, filename='2210.09643_6-10.pdf', object='file',
    # purpose='assistants', status='processed', status_details=None), FileObject( ...
    ids = re.findall(r"id='(.*?)'", input_string)
    # clean up
    for i in range (0, len(ids)):
        print('Deleting file id:', ids[i])
        client.files.delete(ids[i])

# boilerplate code
env_var = os.getenv('OPENAI_API_KEY')
print(env_var)
client = OpenAI()
models = client.models.list()
print(models)


# this should be in a loop on the client side, but for now we will just do it once
filepath = find_file_path('2210.09643.pdf', '/home/daniel/git/icml2023/')
assistant1, file_id = create_assistant(filepath)


print(file_id)

client.files.list()

show_json(assistant1)

assistant_id = assistant1.id
assistant_query = "Name the file you are able to assist me with, list the sections and summarise the content"
assistant_reply = get_assistant_response(assistant_id, assistant_query)
model_dict = assistant_reply.model_dump()


for key, value in model_dict.items():
    print(f"Key: {key}, Data Type: {type(value)}")

for key, value in model_dict.items():
    print(f"Key: {key}, Value: ", end="")
    if isinstance(value, list):
        print()
        for i, item in enumerate(value):
            if isinstance(item, dict):
                for sub_key, sub_value in item.items():
                    print(f"\tSub-key: {sub_key}, Sub-value: {sub_value}")
            else:
                print(f"  Item {i}: {item}")
    else:
        print(value)

# output
# Note, we need to get to subkey value 'quote'
        
# Key: data, Value: 
# 	Sub-key: id, Sub-value: msg_w9NbdbJ1WMuPstJUP3IGekl6
# 	Sub-key: assistant_id, Sub-value: None
# 	Sub-key: content, Sub-value: [{'text': {'annotations': [], 'value': 'Name the file you are able to assist me with, list the sections and summarise the content'}, 'type': 'text'}]
# 	Sub-key: created_at, Sub-value: 1706469479
# 	Sub-key: file_ids, Sub-value: []
# 	Sub-key: metadata, Sub-value: {}
# 	Sub-key: object, Sub-value: thread.message
# 	Sub-key: role, Sub-value: user
# 	Sub-key: run_id, Sub-value: None
# 	Sub-key: thread_id, Sub-value: thread_XhhPoZk5xGSuJd39hsAmKfjf
# 	Sub-key: id, Sub-value: msg_8oID98jvbB0H9v05aEe81oGn
# 	Sub-key: assistant_id, Sub-value: asst_b5ximPpydXXPSvlYxO1zeIVc
# 	Sub-key: content, Sub-value: [{'text': {'annotations': [{'end_index': 1331, 'file_citation': {'file_id': 'file-fU81ZXUaovfgOGNw4k8oG3Qo', 'quote': 'Improving Adversarial Robustness Through the
                                                                                                       
#Key: data, Value: 
#  Item 0: {'id': 'msg_w9NbdbJ1WMuPstJUP3IGekl6', 'assistant_id': None, 'content': [{'text': {'annotations': [], 'value': 'Name the file you are able to assist me with, list the sections and summarise the content'}, 'type': 'text'}], 'created_at': 1706469479, 'file_ids': [], 'metadata': {}, 'object': 'thread.message', 'role': 'user', 'run_id': None, 'thread_id': 'thread_XhhPoZk5xGSuJd39hsAmKfjf'}
#  Item 1: {'id': 'msg_8oID98jvbB0H9v05aEe81oGn', 'assistant_id': 'asst_b5ximPpydXXPSvlYxO1zeIVc', 'content': [{'text': {'annotations': [{'end_index': 1331, 'file_citation': {'file_id': 'file-fU81ZXUaovfgOGNw4k8oG3Qo', 'quote': 'Improving Adversarial Robustness Through the Contrastive-Guided Diffusion Process\n\n\n2020) and its accelerated variant Denoising Diffusion Im-\nplicit Model (DDIM) (Song et al. 2021a). In the following\nwe briefly review the key components of DDPM.\nThe core of DDPM is a forward Markov chain with Gaussian\ntransitions distributions q(xt\n|xt−1\n) to inject Gaussian noise\nto the original data distribution q(x0\n). More specifically\n(Ho et al. 2020) model the forward Gaussian transition as:\nq (xt\n|xt−1\n) := N \n√\n(  αt\nxt−1\n (1 − αt\n) I) \nwhere αt\n t  = 1 2 . . .  T is a decreasing sequence\nto control the variance of injected noise and I is the\nidentity covariance matrix. The joint likelihood for\nthe above Markov chain can be written as q (x0:T \n) =\nq (x0\n)  T\nt=1 \nq (xt\n|xt−1\n).  DDPM then propose to use\npθ \n(x0:T \n) = pθ \n(xT \n)  T\nt=1 \npθ \n(xt−1\n|xt\n) to model the re-\nverse process where pθ\n(xt−1\n|xt\n) is parameterized using a\nneural network. The training objective is to minimize the\nKullback–Leibler (KL) divergence between the forward and\nreverse process: DKL \n(q (x0:T \n)  pθ \n(x0:T \n)) which can be\nsimplified as:\n\n\nmin\nθ \nEtx0ϵ \n√  √\nϵ − ϵθ \nα¯t\nx0 \n+ 1 − α¯t\nϵ t  2 \n\n\n\nwhere the expectation is taken with respect to x0 \n∼ q(x0\n)\nϵ ∼ N(0 I) and t uniformly distributed in {1 . . .  T}.\nHere\nwork parameterized by\nα¯t \n= ts\n=1 \nαs \nand\nθ. \nϵθ\n(x t) denotes the neural net-\nWe refer to (Ho et al. 2020) for\nthe detailed derivation and learning algorithms.\nAfter learning the time-reversed process parameterized by\nθ the original generation process in (Ho et al. 2020) is a\ntime-reversed Markov chain as follows:\n\n\nxt−1 \n= √\n1\nαt \nxt \n− √\n1 − αt\n1 − α¯t \nϵθ \n(xt\n t)  + σt\nzt\n\n\n\nstarting from xT \n∼ N(0 I) and calculating for t = T T −\n1 . . .  1.  The output value x0 \nis the generated synthetic\ndata. Here zt \n∼ N(0 I) if t > 1 and zt \n= 0 if t = 1.\nDDIM (Song et al. 2021a) speeds up the above procedure\nby generalizing the diffusion process to a non-Markovian\nprocess leading to a sampling trajectory much shorter than\nT\nq \n. DDIM\n(xt\n|x0\n) \ncarefully designs the\n= N \n√\nαt\nx0\n (1 − \nforward transition\nαt\n) I for all t = \nsuch that\n1 . . .  T.\n        


# things we want to do
# 1. get the path to a pdf file
# 2. pass the path to openai
# 3. get the file.id back when file is uploaded
# 4. Make queries
# 5. Delete the file id when we are done

# on the client side
# 1. instantiate the class
# 2. get the file ids we are interested in
# 3. get paths from file ids plus metadata e.g. abstract, bibtex

# pseudo code

# open pickle file

# class OpenAIWrapper:
#     def __init__(self, api_key):
#         self.api_key = api_key

#     def set_api_key(self, api_key):
#         self.api_key = api_key

#     def get_api_key(self):
#         return self.api_key

#     def query(self, query):
#         # Implement your logic here to process the query using OpenAI API
#         # and return the response as a string
#         return "Response to query: " + query

# # Example usage:
# openai_wrapper = OpenAIWrapper('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')
# response = openai_wrapper.query("What is the capital of France?")
# print(response)
