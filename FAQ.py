import streamlit as st
import pandas as pd
import ast
import openai
from openai.embeddings_utils import cosine_similarity

# Replace with your OpenAI API key
openai.api_key =  st.secrets["mykey"]

df = pd.read_csv("qa_dataset_with_embeddings.csv")
df['Question_Embedding'] = df['Question_Embedding'].apply(ast.literal_eval)


def get_embedding(text, model="text-embedding-ada-002"):
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

def find_best_answer(user_question):
   # Get embedding for the user's question
   user_question_embedding = get_embedding(user_question)

   # Calculate cosine similarities for all questions in the dataset
   df['Similarity'] = df['Question_Embedding'].apply(lambda x: cosine_similarity(x, user_question_embedding))

   # Find the most similar question and get its corresponding answer
   most_similar_index = df['Similarity'].idxmax()
   max_similarity = df['Similarity'].max()

   # Set a similarity threshold to determine if a question is relevant enough
   similarity_threshold = 0.6  # You can adjust this value

   if max_similarity >= similarity_threshold:
      best_answer = df.loc[most_similar_index, 'Answer']
      return best_answer
   else:
      return "I apologize, but I don't have information on that topic yet. Could you please ask other questions?"

def main():
    st.title("Question Answering App")

    user_input = st.text_input("Ask your question:")
    submit_button = st.button("Submit")

    if submit_button:
        if user_input:
            answer = find_best_answer(user_input)
            st.write(answer)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()


