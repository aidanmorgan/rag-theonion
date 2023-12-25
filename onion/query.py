from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector


model = SentenceTransformer('all-MiniLM-L6-v2')

conn = psycopg2.connect(database="rag_scratch",
                        host="192.168.1.110",
                        user="postgres",
                        port="5432")
register_vector(conn)


def main():
    q = input('Enter query: ')

    cur = conn.cursor()

    embedded = model.encode(q)

    cur.execute("SELECT title, body FROM onion_articles ORDER BY embedding <-> %s LIMIT 5;", (embedded,))
    results = cur.fetchall() 

    for row in results:
        print('------ ARTICLE ------')
        print(row) 
        print('------ END ARTICLE ------')



if __name__ == '__main__':
    main()