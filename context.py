import nai


class ContextHandler:
    def __init__(self,client):
        self.client = client
        self.actions = []
        self.maximum_context = 984
        self.memory = {'text':'','tokens':0}

    def set_memory(self, memory):
        token_len = buffer_encoded = self.client.encoder.tokenizer(memory, 
            return_tensors="pt",padding=True)['input_ids'].shape[1]
        self.memory = {'text':memory,'tokens':token_len}

    def commit_action(self, action):
        token_len = buffer_encoded = self.client.encoder.tokenizer(action, 
            return_tensors="pt",padding=True)['input_ids'].shape[1]
        self.actions.append({'text':action,'tokens':token_len})
    
    def undo_action(self):
        self.actions = self.actions[:-1]

    def get_context(self):
        available_tokens = self.maximum_context - self.memory['tokens']
        context = ""
        for action in reversed(self.actions):
            available_tokens -= action['tokens']
            if available_tokens <= 0:
                break
            context = action['text'] + context
        context = self.memory['text'] + context
        print(context)
        return context

    def generate(self):
        result = self.client.generate(self.get_context())
        self.commit_action(result)
        return result
