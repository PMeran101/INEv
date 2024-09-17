import pickle


def save_file(fileName: str,content):
    """
    Save bianry file to current dir
    :param fileName: file name
    :param content: content to save
    """
    with open(fileName,'wb') as f:
        pickle.dump(content,f)
        

def load_file(fileName: str):
    """
    Load binary file from current dir
    :param fileName: file name
    :return: content of file
    """
    with open(fileName,'rb') as f:
        return pickle.load(f)