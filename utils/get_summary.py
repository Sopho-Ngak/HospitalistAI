import os
import openai


def get_summary_from_openai(text):
    text += "\n\nInstructions: You can make use of paragraphs if needed, make use of html tags to make the text more readable."
    try:
        openai.api_key = os.getenv("API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                {
                    "role":"system", "content":"Your are a good specialist doctor to summarize patient discharge note",
                    "role": "user", "content": text,
                }
            ]
        )

        return str(response["choices"][0]["message"]["content"])
    except Exception as e:
        with open("ai_error.log", "a") as f:
            f.write('\n'+str(e))
        return "Sorry, HospitalistAI is getting many requests right now from different doctors arround the world. Please try again."

