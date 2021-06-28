import torch
from transformers import GPT2TokenizerFast
import base64

class NAIEncoder:

    def __init__(self):
        self.tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
        self.tokenizer.pad_token_id = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"

    def encode_text(self,text):
        bytes = list(map(lambda x: x.to_bytes(2,"little"), 
                            self.tokenizer(text, return_tensors="pt",
                            padding=True).input_ids.tolist()[0]))

        bytes = b''.join(bytes)
        return base64.b64encode(bytes).decode("utf-8")

    def decode_text(self,basetext):
        bytes = base64.b64decode(basetext)
        ids = [[ bytes[i*2] + bytes[(i*2)+1]*256 for i in range(len(bytes)//2) ]]
        tens = torch.tensor(ids)
        result = self.tokenizer.batch_decode(tens)
        return result[0]