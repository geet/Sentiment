import re
def remove_links(tokens):
    for token in tokens:
        if(re.match("^((ht|f)tp(s?)\:\/\/|~/|/)?([\w]+:\w+@)?([a-zA-Z]{1}([\w\-]+\.)+([\w]{2,5}))(:[\d]{1,5})?((/?\w+/)+|/?)(\w+\.[\w]{3,4})?((\?\w+=\w+)?(&\w+=\w+)*)?",token)):
            tokens.remove(token)
    return tokens

def remove_names(tokens):
    for token in tokens:
        if(re.match('@',token)):
            tokens.remove(token)
    return tokens

def remove_noise_words(tokens):
        lines = [line.strip() for line in open("noise_words")]
        for word in lines:
            if(word in tokens):
                tokens.remove(word)
        print(tokens)
        return tokens


