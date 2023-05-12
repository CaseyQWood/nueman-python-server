import os

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat(prompt): 

  completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ],
    )

  return completion.choices[0].message


  