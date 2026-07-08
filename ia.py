import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def responder(pergunta):

    resposta = client.responses.create(
        model="gpt-5",
        input=f"""
Você é o assistente inteligente do sistema SmartLab.

Você ajuda usuários a:

- cadastrar ativos
- abrir ordens de serviço
- movimentar equipamentos
- tirar dúvidas
- explicar funcionalidades

Responda sempre em português.
Pergunta:

{pergunta}
"""
    )

    return resposta.output_text