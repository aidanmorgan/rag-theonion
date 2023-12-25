
```
mistral: https://files.mistral-7b-v0-1.mistral.ai/mistral-7B-v0.1.tar
```

# Download the onlion articles
Download to `./onion/out`

```
https://huggingface.co/datasets/Biddls/Onion_News/tree/main
```

# Run a postgres database with the pgvector extension
``` bash
docker run -it -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 ankane/pgvector
```

# Create the create the database
```sql
CREATE EXTENSION vector;

CREATE TABLE onion_articles (
                                id serial primary key,
                                title text not null,
                                body text not null,
                                embedding vector(384)
);
```

# Seed the vector database
```
cd onion
pip -U -r requirements.txt
python seed.py
```

# Run the model
```
cd mistral
pip -U -r requirements.txt
python mistral.py
```
