from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer('all-MiniLM-L6-v2')

def main():
    val = input("Enter string to encode: ")

    encoded = model.encode(val, )

    print(f"------ BEGIN EMBEDDING ({len(encoded)} tokens)------")
    print(encoded)
    print("------ END EMBEDDING ------")


if __name__ == '__main__':
    main()