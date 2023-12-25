from ctransformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
from langchain.chains import LLMChain
from langchain.schema.document import Document
from langchain.prompts import PromptTemplate


article_model = SentenceTransformer('all-MiniLM-L6-v2')

conn = psycopg2.connect(database="rag_scratch",
                        host="192.168.1.110",
                        user="postgres",
                        port="5432")
register_vector(conn)

template = """
                You will be given a series of articles which will be  enclosed in triple backticks (```). 
                The title of the article will be enclosed by <title> and </title> tags.
                The body of the article will be enclosed by <body> and </body> tags. 
                You will also be provided a question enclosed in double backticks(``).
                Using only the article information supplied, provide an answer to the question in as much detail as possible.
                Your answer should be less than 300 words.
                Your answer humour should be considered acerbic or black humour and use a similar style of humour to the provided articles.

                Articles:
                ```{text}```


                Question:
                ``{creative_prompt}``


                Answer:
                """

prompt = PromptTemplate(template=template, input_variables=["context", "creative_prompt"])


print("Loading Mistral model.")
MODEL_NAME = "mistralai/Mistral-7B-v0.1"

tokenizer = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
print("Created tokenizer.")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
print("Created model.")


llm = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
    repetition_penalty=1.1,
    temperature=0.7,
    return_full_text=True,
    max_new_tokens=100,
)

print("Created LLM")


def main():
    creative_prompt = ''

    while(creative_prompt != "q!"):
        creative_prompt = input("Enter a theme (or q! to quit): ")

        cur = conn.cursor()
        embedded = article_model.encode(creative_prompt)

        cur.execute("SELECT title, body FROM onion_articles ORDER BY embedding <-> %s LIMIT 5;", (embedded,))
        results = cur.fetchall() 

        if(len(results) == 0):
            print("Couldn't find any matching articles for inspiration")
        else:
            docs = [Document(page_content=f"<title>{t[0]}</title><body>{t[1]}</body>") for t in results]

            llm_chain = LLMChain(prompt=prompt, llm=llm)
            answer = llm_chain.run({
                "context": docs,
                "creative_prompt": creative_prompt,
            })



            print(answer)


if __name__ == '__main__':
    main()