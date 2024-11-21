from openai import OpenAI
import json
import os


class TestGeneration:
    def __init__(self):
        #TODO make the key acceptable through .env
        # self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_key = ""

    def chat_conversation(self, data):
        client = OpenAI(api_key=self.openai_api_key)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"Please generate tests for {data}"},
                {"role": "system",
                 "content": "You are a Senior QA Engineer (tester) with 20 years of working experience."
                            " Your task is to make the absolutely functional and comprehensive in terms of"
                            " edge cases test class for the documentation in .json the user presents to you."
                            " Please output only solely Python code without anything else. It is strictly."
                            " Please note that the service is already running on the localhost on the 5000 port."}
            ]
        )
        return completion.choices[0].message.content
