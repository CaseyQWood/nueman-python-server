import os
import openai
from tqdm.auto import tqdm  # this is our progress bar
from datasets import load_dataset
openai.api_key = os.getenv("OPENAI_API_KEY")

import pinecone
pinecone.init(
  api_key=os.getenv("PINECONE_API_KEY"), 
  environment=os.getenv("PINECONE_ENVROMENT")
)



def get_embedding(prompt): 
  # load the first 1K rows of the TREC dataset
  trec = load_dataset('trec', split='train[:1000]')

  response = openai.Embedding.create(
      input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"],
      model="text-embedding-ada-002"
  )
  embeds = [record['embedding'] for record in response['data']]
  # print("Embeddings1: ", embeds, " Length: ", len(embeds))

    # check if 'openai' index already exists (only create index if not)
  if 'openai' not in pinecone.list_indexes():
    pinecone.create_index('openai', dimension=len(embeds[0]))
  # connect to index
  index = pinecone.Index('openai')
  print("Index: ", index)

  query = "Why was there a long-term economic downturn in the early 20th century?"

  xq = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
  # print("xq: ", xq)

  res = index.query([xq], top_k=5, include_metadata=True)
  
  for match in res['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")

  # batch_size = 32  # process everything in batches of 32
  # for i in tqdm(range(0, len(trec['text']), batch_size)):
  #     print("i: ", i)
  #     # set end position of batch
  #     i_end = min(i+batch_size, len(trec['text']))
  #     print("i_end: ", i_end)
  #     # get batch of lines and IDs
  #     lines_batch = trec['text'][i: i+batch_size]
  #     print("lines_batch: ", lines_batch)
  #     ids_batch = [str(n) for n in range(i, i_end)]
  #     # create embeddings
  #     res = openai.Embedding.create(input=lines_batch, engine="text-embedding-ada-002")
  #     embeds = [record['embedding'] for record in res['data']]
  #     print("embeds: ", embeds)
  #     # prep metadata and upsert batch
  #     meta = [{'text': line} for line in lines_batch]
  #     print("meta: ", meta)
  #     to_upsert = zip(ids_batch, embeds, meta)
  #     print("to_upsert: ", to_upsert)
  #     # upsert to Pinecone
  #     index.upsert(vectors=list(to_upsert))


  embeddings = response['data'][0]['embedding']
  # print("Embeddings2: ", embeddings, " Length: ", len(embeddings))
  return embeddings



