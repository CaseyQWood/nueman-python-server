import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def chat(prompt): 

  completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ],
    )

  return completion.choices[0].message


  