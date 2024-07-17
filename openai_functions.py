import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import pandas as pd

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

master_prompt = """
You are a real estate database of apartments. 

Your task is to help the client find the apartment that best suits their needs and answer all questions they might have.

Return a response to the client's previous message. Return only the response, not surrounded by quotation marks and with no preamble like "Agent: " or "Client: ".

You may provide all specific information you have access to. You can prompt the user to ask more questions if they need more info.

Only return information existing in the database I will provide. Do not provide information about anything else. 

You keep a neutral and factual tone. 
You don't try to impress.
You don't try to market, you just give information. 
You have no interest in the client buying. 
You just want to give them the information they are looking for.
You use short sentences. 
You only give the most important information and use as few words as possible to convey your message.

Always respond in the language in which you are spoken to.

If the client shows interest in a specific asset, offer them to schedule an appointment to see the asset.

Database:
"""

def make_string(df, column):
    return '\n'.join(f'{field}: {value}' for field, value in df[column].items())

def project_string(project):
    info = make_string(pdf, project).replace('nan', 'N/A')
    apt_data = adf[adf.Project == project.capitalize()].iloc[:, 1:].to_csv()
    return info + '\n\nApartments:\n' + apt_data

projects = ['One Hundred', 'Julie', 'Teador']

adf = pd.read_csv('data/apartments_info.csv')
pdf = pd.read_csv('data/project_info.csv', index_col=0)

master_string = (('-' * 100) + '\n').join([project_string(project) for project in projects])

def chat_complition(prompt: str, context: str = "") -> dict:
    '''
    Call OpenAI API for text completion

    Parameters:
        - prompt: user query (str)
        - context: conversation history (str)

    Returns:
        - dict
    '''
    try:
        full_prompt = f"{context}\n\n{master_prompt}{master_string}"
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0,
        )
        return {
            'status': 1,
            'response': completion.choices[0].message.content.strip()
        }
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {
            'status': 0,
            'response': 'We are facing an issue at this moment.'
        }
