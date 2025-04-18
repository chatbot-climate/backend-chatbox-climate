import numpy as np
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('all-MiniLM-L6-v2')

def find_closest_answer(question, index, sentences):
    query_embedding = model.encode([question], convert_to_tensor=True).cpu()
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k=1)
    responses = [sentences[i] for i in indices[0]]
    

    return {
        "question_trouvee": "\n".join(responses),
        "score": distances
    }