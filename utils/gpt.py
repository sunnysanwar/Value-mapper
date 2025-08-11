from connections.open_ai import auth_openai
from src.const import GPT_MODEL, PRIMER
import gradio as gr
import re
from src.const import EMBED_MODEL
from sklearn.metrics.pairwise import cosine_similarity

openai = auth_openai()

def create_embedding(data):
    embeddings = openai.Embedding.create(input=data, engine=EMBED_MODEL)
    embeddings = [embeddings['data'][i]['embedding'] for i in range(len(embeddings['data']))]
    return embeddings

def gpt_suggest_keywords(user_keyword, keywords, keywords_embedding, temp=1):
    keywords = "\n".join(keywords)
    if user_keyword:
        prompt = f"List of Keywords:\n{keywords}\n\nUser Keyword:\n{user_keyword}\n\nPlease provide the relevant and similar keywords."
        response = openai.ChatCompletion.create(
            temperature=temp,
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": PRIMER},
                {"role": "user", "content": prompt}
            ]
        )['choices'][0]['message']['content']
        if "," in response:
            response_keywords = response.split(",")[1:]
        else:
            response_keywords = response.split("\n")[1:]
        response_keywords = [re.sub("[-\.]", "", keyword).strip() for keyword in response_keywords if keyword]
        response_keywords = [re.sub("[0-9]+", "", keyword).strip() for keyword in response_keywords]
        keywords = keywords.split("\n")
        response_keywords_embedding = create_embedding(response_keywords)
        cos_scores = cosine_similarity(response_keywords_embedding, keywords_embedding)
        up_keywords = {}
        for r in range(len(response_keywords)):
            for i, keyword in enumerate(keywords):
                score = float(cos_scores[r][i])
                if score > 0.88:
                    if response_keywords[r].lower() in keyword.lower():
                        up_keywords.update({keyword: 1.0})
                    elif keyword in up_keywords and up_keywords[keyword] < score:
                        up_keywords.update({keyword: score})
                    elif keyword not in up_keywords:
                        up_keywords.update({keyword: score})
        up_keywords = sorted(up_keywords.items(), key=lambda x: x[1], reverse=True)
        up_keywords = [keyword for keyword, _ in up_keywords]
        return up_keywords
    else:
        raise gr.Error('Type the input')