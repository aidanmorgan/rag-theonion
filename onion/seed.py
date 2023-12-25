from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector


model = SentenceTransformer('all-MiniLM-L6-v2')

__CURSOR_BATCH_SIZE__ : int = 50


def main():
    with open("NewsWebScrape.txt", mode="r", encoding="utf-8") as f:
        count = 0

        for line in f:
            print(".")
            if count % __CURSOR_BATCH_SIZE__ == 0:
                if count > 0:
                    conn.commit()
                    cur.close()
                    conn.close()
                    print(f"Saved {count} embeddings.")


                conn = psycopg2.connect(database="rag_scratch",
                                        host="localhost",
                                        user="postgres",
                                        port="5432")
                register_vector(conn)
                cur = conn.cursor()


            cleaned = line.rstrip()
            vals = cleaned.split("#~#")

            if len(vals) == 2:
                encoded_body = model.encode(cleaned)

                cur.execute("INSERT INTO onion_articles (title, body, embedding) VALUES (%s, %s, %s)", (vals[0], vals[1], encoded_body.tolist()))
                count += 1

        conn.commit()
        cur.close()
        conn.close()
        print(f"Saved {count} embeddings.")
            




if __name__ == "__main__":
    main()