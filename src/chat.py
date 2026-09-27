from search import search_prompt

from dotenv import load_dotenv

load_dotenv()


def main():

    question = input("Digite sua pergunta: ")

    chain = search_prompt(question)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print(chain)

    main()

if __name__ == "__main__":
    main()