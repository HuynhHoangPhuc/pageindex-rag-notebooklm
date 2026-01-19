from pageindex import PageIndexClient
import inspect

print("Method signatures for PageIndexClient:")
print("chat_completions:", inspect.signature(PageIndexClient.chat_completions))
print("submit_query:", inspect.signature(PageIndexClient.submit_query))
