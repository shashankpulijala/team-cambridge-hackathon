from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import pandas as pd


class Message(Model):
    message: str


class Response(Model):
    response: str


parser_address = 'agent1qgtvev96vtf05f9jlhn7mu94vku9l7ncleuacmyef8fljrg5jwt0qs7sgll'

premium = Agent(name="premium", seed="khasdljghfgfd", port=5003, endpoint=['http://localhost:5003/submit'])

fund_agent_if_low(premium.wallet.address())


@premium.on_event('startup')
async def user_handler(ctx: Context):
    ctx.logger.info(f'My address is {premium.address}')


@premium.on_message(model=Message)
async def parse_doc(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    # Define the dataset
    data = {
        "insurance_policy": ["tranches"],
        "frequency_of_payment": ['monthly']
    }

    df = pd.DataFrame(data)

    # Apply the conditions to the dataset
    conditions_code = msg.message

    # Remove triple backticks from conditions_code
    conditions_code = conditions_code.replace("```", "")

    # Evaluate conditions on the dataset
    insurance_quotes = []
    print(df.head())
    for index, row in df.iterrows():
        insurance_quote = []
        row_dict = row.to_dict()
        locals().update(row_dict)
        ctx.logger.info(f"Evaluating conditions for row {index}: {row_dict}")
        try:
            exec(conditions_code)
        except NameError as e:
            ctx.logger.warning(f"Skipping condition due to missing variable: {e}")
        ctx.logger.info(f"Generated insurance quote for row {index}: {insurance_quote}")
        insurance_quotes.append(insurance_quote)

    df['insurance_quote'] = insurance_quotes

    # Extract the specific insurance quote
    specific_quotes = [quote for quotes in df['insurance_quote'] for quote in quotes if quote]

    # Print the results
    ctx.logger.info(df.to_string())
    final_response = specific_quotes[-1] if specific_quotes else "No specific insurance quote available"
    await ctx.send(parser_address, Response(response=final_response))


if __name__ == "__main__":
    premium.run()
