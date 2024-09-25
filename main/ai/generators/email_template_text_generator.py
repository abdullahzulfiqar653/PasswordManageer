from textwrap import dedent
from pydantic.v1 import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from main.ai import config
from main.ai.generators.utils import ParserErrorCallbackHandler


def get_email_rephrase_chain():
    class EmailSchema(BaseModel):
        body: str

    system_prompt = dedent(
        """
        You are tasked with rewriting an email in the style of {{REWRITING_TEMPLATE}}.
        Use technological language, a visionary tone, and strict brevity.
        Keep sentences short, direct, and avoid unnecessary elaboration.
        Do not alter the meaning or engage in a dialogue with the content.
        Just rephrase the email according to the following style guidelines:

        - **Technological Language**: Incorporate words related to technology, innovation, or science.
        - **Strict Brevity and Directness**: Use short, direct sentences. Prioritize concise expression.
        - **Optimism and Visionary Tone**: Reflect ambition, confidence, and a vision for the future.
        - **Optional Humor or Light Sarcasm**: Add a subtle humorous touch if appropriate.
        - **Vision of the Future**: Emphasize big plans, technological advancements, or the future of humanity.

        Original email content:
        <email_content>
        {{EMAIL_CONTENT}}
        </email_content>

        Your output should be the rewritten email in the style of {{REWRITING_TEMPLATE}}.

        Provide the rephrased email in JSON format:
        {
            "body": "<Rephrased Body>"
        }
        """
    )

    llm = ChatOpenAI(model=config.model)
    prompt = ChatPromptTemplate.from_messages(
        [("human", system_prompt)], template_format="jinja2"
    )
    parser = PydanticOutputParser(pydantic_object=EmailSchema)
    chain = prompt | llm.bind(response_format={"type": "json_object"}) | parser
    return chain


def generate_email_message(template, email_content):
    response = get_email_rephrase_chain().invoke(
        {
            "EMAIL_CONTENT": email_content,
            "REWRITING_TEMPLATE": template,
        },
        config={"callbacks": [ParserErrorCallbackHandler()]},
    )

    rephrased_email = response.dict()
    return rephrased_email["body"]
