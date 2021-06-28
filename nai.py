import requests
import json
import encoding

class NAIClient:
    def __init__(self, authtoken):
        self.encoder = encoding.NAIEncoder()
        self.authtoken = authtoken

    def generate(self,text,params={}):

        encoded_text = self.encoder.encode_text(text)

        data = {
            "input": encoded_text,
            "model": "6B",
            "parameters":
            {
                "temperature": 0.85,
                "max_length": 83,
                "min_length": 63,
                "top_k": 30,
                "top_p": 0.9,
                "tail_free_sampling": 1,
                "repetition_penalty": 1.135,
                "repetition_penalty_range": 512,
                "repetition_penalty_slope": 3.33,
                "bad_words_ids": [[0]],
                "use_cache": False,
                "return_full_text": False
            }
        }

        for k in params.keys():
            data["parameters"][k] = params[k]

        r = requests.post("https://api.novelai.net/ai/generate",
                          data=json.dumps(data), headers={
                            'Content-type': 'application/json',
                            'accept': 'application/json',
                            'Authorization': 'Bearer {}'.format(self.authtoken)
                          })

        jsonres = r.json()

        if "statusCode" in jsonres:
            raise Exception(jsonres["statusCode"],jsonres["message"])
        if "error" in jsonres:
            raise Exception(jsonres["error"])

        return self.encoder.decode_text(jsonres["output"])
