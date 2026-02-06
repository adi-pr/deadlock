import boto3
import json
import re

def instanciate_agent(message, prompt, strip_markup=True):
    client = boto3.client("bedrock-runtime", region_name="eu-west-2") # our model is limited to whats available in the region

    response = client.invoke_model(
        modelId="deepseek.v3-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "messages": [
                {
                    "role": "system",
                    "content": [
                        { "type": "text", "text": message } # system instructions 
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": prompt } # tasking 
                    ]
                }
            ],
            "temperature": 0.0, # 0.0 is deterministic and will be exactly what we want so dont touch
            "top_p": 0.9,
            "max_tokens": 512
        })
    )
    
    result = json.loads(response["body"].read().decode("utf-8"))

    # get the content of the message 
    text = result["choices"][0]["message"]["content"]
    
    # strip the markup out of the response
    if strip_markup:
        clean_output = re.sub(r"^```(?:python)?\n|```$", "", text, flags=re.MULTILINE)
        return clean_output
    else:
        return text
    
