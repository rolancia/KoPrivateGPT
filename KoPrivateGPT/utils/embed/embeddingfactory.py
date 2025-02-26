from enum import Enum
from dotenv import load_dotenv
import os
from KoPrivateGPT.utils import text_modifier


class EmbeddingType(Enum):
    OPENAI = 'openai'
    KOSIMCSE = 'kosimcse'
    KO_SROBERTA_MULTITASK = 'ko-sroberta-multitask'


class EmbeddingFactory:
    def __init__(self, embed_type: str, device_type: str = 'cuda'):
        load_dotenv()
        if embed_type in text_modifier('openai'):
            self.embed_type = EmbeddingType.OPENAI

        elif embed_type in text_modifier('kosimcse',
                                         modify_words=['KoSimCSE', 'KoSimcse', 'koSimCSE', 'kosimCSE']):
            self.embed_type = EmbeddingType.KOSIMCSE
        elif embed_type in text_modifier('ko_sroberta_multitask'):
            self.embed_type = EmbeddingType.KO_SROBERTA_MULTITASK
        else:
            raise ValueError(f"Unknown embedding type: {embed_type}")

        if device_type in text_modifier('cpu'):
            self.device_type = 'cpu'
        elif device_type in text_modifier('mps'):
            self.device_type = 'mps'
        else:
            self.device_type = 'cuda'

    def get(self):
        if self.embed_type == EmbeddingType.OPENAI:
            openai_token = os.getenv("OPENAI_API_KEY")
            if openai_token is None:
                raise ValueError("OPENAI_API_KEY is empty.")
            try:
                from langchain.embeddings import OpenAIEmbeddings
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not import OpenAIEmbeddings library. Please install OpenAI library."
                    "pip install openai"
                )
            return OpenAIEmbeddings(openai_api_key=openai_token)

        elif self.embed_type == EmbeddingType.KOSIMCSE:
            try:
                from langchain.embeddings import HuggingFaceEmbeddings
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not import HuggingFaceEmbeddings library. Please install HuggingFace library."
                    "pip install sentence_transformers"
                )
            return HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta-multitask",
                                         model_kwargs={"device": self.device_type})
        elif self.embed_type == EmbeddingType.KO_SROBERTA_MULTITASK:
            try:
                from langchain.embeddings import HuggingFaceEmbeddings
            except ImportError:
                raise ModuleNotFoundError(
                    "Could not import HuggingFaceEmbeddings library. Please install HuggingFace library."
                    "pip install sentence_transformers"
                )
            return HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask",
                                         model_kwargs={"device": self.device_type})
        else:
            raise ValueError(f"Unknown embedding type: {self.embed_type}")
