import pickle
import numpy as np
import faiss
import torch

# https://donnees.banquemondiale.org/theme/changement-climatique?utm_source=chatgpt.com V1
# https://databank.worldbank.org/ V2

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open("models_nlp/final/climatique_embeddings.pkl", "rb") as f:
    # data = torch.load(f, map_location=device, weights_only=False)
    # data = torch.load(f, map_location=device)
    data = pickle.load(f)
    sentences = data["sentences"] # liste de questions/réponses pré-définies

    embeddings = data["embeddings"] # vecteurs d'embedding
    
    if isinstance(embeddings, torch.Tensor):
        embeddings_cpu = (embeddings.cpu() if embeddings.is_cuda else embeddings).numpy()
    else:
        embeddings_cpu = embeddings

    embedding_dim = embeddings_cpu.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(embeddings_cpu, dtype=np.float32))