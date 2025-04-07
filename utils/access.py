#A file for storing and retriving varriables accross the project

def set_retriever(ret):
    global retriever  # ✅ Use the same name here
    retriever = ret

def get_retriever():
    return retriever  # ✅ And here!
