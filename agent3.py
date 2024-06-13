from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low
from docx import Document
import openai
import pandas as pd
import re

premium_address = 'agent1qdj0qess34rgraz2w40qa2xa7wggvvw4gmnqh09cff4kkgj9zme8gl8s0xm'

class Message(Model):
    message: str

openai.api_key = '###'

rules = Agent(name="rules", seed="khljghfgfd",port = 5002, endpoint = ['http://localhost:5002/submit'])

fund_agent_if_low(rules.wallet.address())

@rules.on_event('startup')
async def user_handler(ctx:Context):
    ctx.logger.info(f'My address is {rules.address}')

@rules.on_message(model = Message)
async def parse_doc(ctx: Context, sender:str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    async def generate_conditions(text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Generate a condition statement for an insurance quote based on the following text:"},
                {"role": "user", "content": text}
            ],
            max_tokens=1500,
            temperature=0.5,
        )
        mapped_fields = response['choices'][0]['message']['content'].strip()
        return mapped_fields

    async def generate_if_else_statement(condition):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "Assume you are a python expert. Convert the following condition statement into a properly formatted if-elif statement in Python. Also please do not use nested if else statements. Use and statements instead of it. I only want if and elif (strictly you can use elif for creating the else statement, at no cost bring an else statement, please ensure that the if and elif statements have valid conditions. Please do not make any syntax errors. I want all the if else statements in the format if (insurance_policy == '' or insurance_policy == '' or insurance_policy == '') else: insurance_quote.append() (where the append statements strictly consist of a string. It can be an empty string).If empty if or elif statement is generated use the condition 3>0."},
                      {"role": "user", "content": condition}],
            max_tokens=150,
            temperature=0.5,
        )
        if_else_statement = response['choices'][0]['message']['content'].strip()
        # Ensure proper formatting with newlines and indentation
        formatted_if_else_statement = if_else_statement.replace(":", ":\n    ").replace(" else", "\nelif")
        return formatted_if_else_statement

    async def split_into_sentences(text):
        sentences = re.split(r'(?<=[.!?]) +', text)
        return sentences

    sections = msg.message.split("\n\n")
    data = []
    for section in sections:
        if section.strip():
            lines = section.split("\n")
            title = lines[0].strip()
            content = " ".join(lines[1:]).strip()
            data.append({'Section': title, 'Content': content})

    ctx.logger.info('Section Processed')
    df = pd.DataFrame(data)

    conditions = []
    for content in df['Content']:
        if isinstance(content, str):
            sentences = await split_into_sentences(content)
            for sentence in sentences:
                condition = await generate_conditions(sentence)
                if_else_statement = await generate_if_else_statement(condition)
                conditions.append(
                    {'Sentence': sentence, 'GeneratedCondition': condition, 'IfElseStatement': if_else_statement})

    conditions_df = pd.DataFrame(conditions)
    conditions = "\n\n".join(conditions_df['IfElseStatement'].tolist())
    ctx.logger.info('Generated conditions')

    async def format_if_else_statement(statement):
        statement1 = statement.replace("```python\n", "")
        statement2 = statement1.replace("```", "")

        if " else: " in statement2:
            parts = statement2.split(" else: ")
            if_part = parts[0]
            else_part = parts[1]

            formatted_if_part = if_part.replace(":", ":\n    ")
            formatted_statement = f"{formatted_if_part}\nelse:\n    {else_part}"

            return formatted_statement
        else:
            return statement2

    formatted_lines = [await format_if_else_statement(line) for line in conditions_df['IfElseStatement'].tolist()]

    formatted_conditions = "\n\n".join(formatted_lines)

    # Send the formatted conditions to the premium agent
    await ctx.send(premium_address, Message(message=formatted_conditions))

if __name__ == "__main__":
    rules.run()


