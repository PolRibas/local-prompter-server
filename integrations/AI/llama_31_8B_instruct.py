import torch
import transformers
from .base_ai import BaseAI
from django.conf import settings

class Llama31_8B_InstructAI(BaseAI):
    def __init__(self):
        self.model_code = "Llama-3.1-8B-Instruct"
        self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
        self.pipeline = None

    def load_model(self):
        if self.pipeline is None:
            auth_token = settings.HUGGINGFACE_API_KEY
            self.pipeline = transformers.pipeline(
                "text-generation",
                model=self.model_id,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device_map="auto",
                #auth_token=auth_token, # Descomenta si el modelo requiere auth
            )

    def generate_response(self, messages: list) -> str:
        # messages es una lista de dicts [{"role":"user"|"assistant"|"system","content": str}]
        # El pipeline espera un formato similar
        # Si el pipeline de HF soporta mensajes tipo chat directamente, se pasa tal cual:
        outputs = self.pipeline(
            messages,
            max_new_tokens=256,
        )
        print('Llama31_8B_InstructAI outputs:', outputs)
        return outputs[0]["generated_text"]

    def get_model_code(self) -> str:
        return self.model_code
