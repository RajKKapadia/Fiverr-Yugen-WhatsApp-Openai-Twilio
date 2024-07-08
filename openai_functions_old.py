import os


from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def chat_complition(prompt: str) -> dict:
    '''
    Call Openai API for text completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:
        # completion = client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        return {
            'status': 1,
            'response': "hi",#completion.choices[0].message.content
        }
    except:
        return {
            'status': 0,
            'response': 'We are facing an issue at this moment.'
        }
