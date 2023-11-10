import os
import openai
import json

# openai.api_key = os.getenv("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")
openai.api_key = "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"

# Define functions here
def get_lastName (p_firstname):
    if p_firstname == "Subhankar":
        v_lastname = "Sarkar";
    return v_lastname;
# print(get_lastName("Subhankar"));

def get_address (p_firstname, p_lastname):
    if p_firstname == "Subhankar" and p_lastname == "Sarkar":
        v_address = "9 Calle Larspur";
    return v_address;
# print(get_address("Subhankar", "Sarkar"));


def run_conversation():
    # Tell AI about the functions available
    messages = [{"role": "user", "content": "What's Subhankar Sarkar's address?"}]
    functions = [
        {
            "name":"get_lastName",
            "description": "get the last name given the first name",
            "parameters": {
                "type": "object",
                "properties": {
                    "p_firstname": {
                        "type": "string",
                        "description": "First name",
                    },
                },
            }
        },
        {
            "name": "get_address",
            "description": "get the address given first name and last name",
            "parameters": {
                "type": "object",
                "properties": {
                    "p_firstname": {
                        "type": "string",
                        "description": "First name",
                    },
                    "p_lastname": {
                        "type": "string",
                        "description": "Last name",
                    },
                },
            }
        }

    ]

    # The first call that ends with finish_reason 'function call'.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    # print(response)
    # print(response_message.get("function_call"))
    # print(response_message["function_call"]["arguments"])


    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_lastName": get_lastName,
            "get_address": get_address,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])

        if function_name == "get_lastname":
            function_response = function_to_call(
               p_firstname=function_args.get("p_firstname")
            )
        if function_name == "get_address":
            function_response = function_to_call(
                p_firstname=function_args.get("p_firstname"),
                p_lastname=function_args.get("p_lastname"),
            )

        # print(function_args.get("p_firstname"))
        print(function_response) # the the thing can end right here


    # 2nd call
    messages.append(response_message)  # extend conversation with assistant's reply
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )  # extend conversation with function response
    second_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    return second_response

# print(run_conversation())
print(run_conversation().choices[0].message.content)