import openai 
from dotenv import find_dotenv , load_dotenv
import os

load_dotenv()


client=openai.OpenAI()
# Get the API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

model="gpt-3.5-turbo-16"

personal_trainer_assis=client.beta.assistants.create(
    name="Personal Ttraier",
    instructions="""you are the best personal trainer and nutritionist who knows how to get clients to build lean muscles.
you've trained high -caliber athletes and movie stars.""",
model=model

)


assistant_id=personal_trainer_assis.id
print(assistant_id)


thread=client.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content":"How do I get started working out"
        }
    ]
)

thread_id=thread.id
