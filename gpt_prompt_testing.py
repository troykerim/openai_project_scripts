from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
    model='ft:gpt-4o-2024-08-06:xxxx:xxxxx:xxxxx',
    # model='gpt-4o-2024-08-06',
    messages=[{
        "role": "system",
         "content": "You are an assistant that does..."},
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Please do something..."},
            {
                "type": "image_url",
                "image_url": {"url": "https://drive.google.com/uc?export=download&id=", "detail": "high"
                              }
            }
        ]
    }],
    max_tokens=8192,  # The maximum with GPT-3 is 4096 including the prompt
    n=1,  # How many results to produce per prompt
    # best_of=1 #When n>1 completions can be run server-side and the "best" used
    # stop=None,
    temperature=0.0
)

print(response.choices[0].message.content)