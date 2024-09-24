from langchain.callbacks.base import BaseCallbackHandler


class ParserErrorCallbackHandler(BaseCallbackHandler):
    def on_chain_start(self, *args, **kwargs):
        if kwargs.get("run_type") == "parser":
            self.ai_message = args[1]

    def on_chain_error(self, *args, **kwargs):
        if hasattr(self, "ai_message"):
            print(self.ai_message)
