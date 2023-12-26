
# What?

An implementation of a Retrieval Augmented Generation (RAG) model, using mistral-7B to generate fake The Onion articles.



## Download the onlion articles
```
cd onion
wget https://huggingface.co/datasets/Biddls/Onion_News/resolve/main/NewsWebScrape.txt
```

## Run a postgres database with the pgvector extension
``` zsh
docker run -it -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 ankane/pgvector
```

This does run the database with no permissions, not for production use!

## Create the create the database

```zsh
docker exec -it {{container id}} bash
psql -U postgres
```

```sql
CREATE DATABASE rag_scratch;

\connect rag_scratch

CREATE EXTENSION vector;
CREATE TABLE onion_articles (
                                id serial primary key,
                                title text not null,
                                body text not null,
                                embedding vector(384)
);
```

## Seed the vector database
``` zsh
cd onion
pip -U -r requirements.txt
python seed.py
```

## Install Ollama

``` zsh
brew install ollama
```

## Register the Modelfile with Ollama

``` zsh
cd mistral
ollama create onion -f Modelfile
```

## Run the model
``` zsh
cd mistral
pip -U -r requirements.txt
python mistral.py
```

