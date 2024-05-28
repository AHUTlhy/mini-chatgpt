from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, max_tokens=2000)
    chain = ConversationChain(llm=model, memory=memory)

    # history包含之前的用户提问以及模型回答，还包含这次用户的提问以及模型的回答
    response = chain.invoke({"input": prompt})
    # print(response) # 返回的是字典。返回的结果包括用户的输入input，还有历史问题history，该history包含了用户输入的prompt，以及模型给出的回答。还有response，是模型的回答
    # 要想获得模型的回答，直接response["response"]
    return response['response']

# memory = ConversationBufferMemory(return_messages=True)
# print(memory)
