import chromadb
import json
import openai
import os
import anthropic

class Model:
    SYS_PROMPT = \
    "Eres parte de un sistema de Retrieval Augmented Generation (RAG). Tu objetivo es resolver las preguntas \
    de los usuarios con respecto a las leyes viales del estado de Jalisco. En un JSON vas a recibir una pregunta \
    y un contexto. Deberás de usar el contexto y únicamente el contexto para contestar la pregunta. Responde en el \
    idioma en el que te preguntaron. Si la pregunta no tiene que ver con leyes viales, recuérdale al usuario tu \
    propósito. Solo si la pregunta tiene que ver con leyes viales, al final de tu respuesta, en una nueva línea, \
    deberás de enlistar los artículos que usaste para responder la la pregunta. La lista de artículos deberá de tener \
    el formato <Nombre de la ley>: Artículo <número de artículo>, y llevará como título 'Para más información, consulta \
    los siguientes artículos:'. Recuerda: enumera los artículos solo si la pregunta tiene que ver con leyes viales."
    
    def __init__(self):
        self._client = chromadb.PersistentClient('model/licenciado_vectordb')
        openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ['OPENAI_API_KEY'],
                model_name="text-embedding-3-small"
            )
        self._collection = self._client.get_collection('master', embedding_function=openai_ef)
        self._anthropic = anthropic.Anthropic()
        
    def _build_user_message(self, q):
        rag = self._collection.query(query_texts=q, n_results=10)
        m = {
            "pregunta": q,
            "contexto": [
                {
                    "ley": metadata['ley'],
                    "numero": metadata['numero'],
                    "titulo": metadata['titulo'],
                    "capitulo": metadata['capitulo'],
                    "texto": articulo
                }
            for articulo, metadata in zip(rag['documents'][0], rag['metadatas'][0])]
        }

        return m
    
    def ask_question(self, q):
        user_message = self._build_user_message(q)
        response = self._anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.0,
            system=Model.SYS_PROMPT,
            messages=[
                {"role": "user", "content": str(user_message)}
            ]
        )
        
        return response.content[0].text, user_message["contexto"]

        
    