import os
import random

master_prompt_ecobuyit = """


You are a customer rep for EcoBuyIt. 

Your task is to give the user information and answer their questions.


If they ask to talk to a human redirect them to the company CEO:


לפרטים נוספים : יונתן הנה – מנכ"ל

טל: 0544982792
yonatanhene@gmail.com


Knowledge base:

{knowledge_base}



Response Instructions:

use spoken language register, not written. write as if you are having a conversation in a house party
use informal daily register
Avoid reusing words or expressions you've already used. find new ways to say the same thing.

"""

kb = open('data/ecobuyit_kb.txt').read()
intro_message = """
שלום וברוכים הבאים לצ'אט בוט החכם של אקובית!
שמי YONIC, ואני כאן כדי לעזור לכם.

תוכלו לשאול אותי כל שאלה שתרצו. אני מבוסס על בינה מלאכותית ולומד ומשתפר כל הזמן.

למה פנייתכם קשורה?
- חשבון מים
- בעיית תשתית
- עדכון מספר נפשות
- דיווח לאקובית, שליחת הודעה או העלאת מסמכים
- נושא אחר שלא מופיע כאן

אני זמין לכל שאלה או בקשה! 😊
"""



master_prompt_ecobuyit = master_prompt_ecobuyit.replace('{knowledge_base}', kb)


#You use playful spins that relate what the user said to your answer in clever humor.
#You sometimes use abbreviations and common colloquial words/expressions. Not classical old ones, but more up to date ones

from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
key = os.getenv("AZURE_OPENAI_API_KEY")
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version="2024-02-01",
    api_key=key
)


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


       
        if len(context) < 5:
            return {
            'status': 1,
            'response': intro_message
        }

        master_prompt_v = master_prompt_ecobuyit
        rand = random.random(); print('rand:', rand)
               
   
        #else:
        #    master_prompt_v = master_prompt.format('Try to schedule for the user a meeting with a human sales representative to discuss purchase of a property the user is interested in.')

        if rand < 0.15:
            master_prompt_v += '\nConsider asking the user something about their interest or motivation for saying the last thing they said'
        elif rand < 0.5:
            master_prompt_v += '\nConsider giving the user one sentence of extra relevant info'
        else:
            master_prompt_v += "\n IMPORTANT: Restrict each message to one short sentence, no more than that. Only provide the most essential pieces of info!!!"

        full_prompt = f"{context.strip()}\n\n{master_prompt_v.strip()}"
        print('context:', context)
        print('--------------------------')
        print('prompt:\n\n', full_prompt.split('\n')[-1])
        print('===============================')
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": full_prompt},
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

