import re
# Ryan Lamb, Miguel Bunag, Troy Lee
# uses regex
def lexer(file_name):
    with open(file_name, 'r') as file:
        code = file.read()

    # this is to categorize it
    tokens = []
    keywords = ["while", "if", "else", "for", "return"] # could of used more keywords like #include for example depending on the C++ code
    separators = ["(", ")", "{", "}", ";"]
    operators = ["+", "-", "*", "/", "=", "<", ">", "=="]
    literals = ["true", "false"]
    identifier_pattern = "[a-zA-Z][a-zA-Z0-9]*"
    real_pattern = "\d+\.\d+"
    integer_pattern = "\d+"

    # to find the patterns
    pattern = "|".join([
        f"({identifier_pattern})",
        f"({real_pattern})",
        f"({integer_pattern})",
        *map(re.escape, separators + operators + literals)
    ])

    # Discovered issue where identifier was taking cadence over keywords so wrote this as a seperation for tokens
    keyword_pattern = "|".join([
        f"\\b{kw}\\b" for kw in keywords
    ])
    
    pattern = f"{keyword_pattern}|{pattern}"

    # to identify the token type and attach it to a lexem
    for match in re.finditer(pattern, code):
        token_type = None
        lexeme = match.group()
        if match.group(1) is not None:
            token_type = "identifier"
        elif match.group(2) is not None:
            token_type = "real"
        elif match.group(3) is not None:
            token_type = "integer"
        
        if token_type is None:
            if lexeme in keywords:
                token_type = "keyword"
            elif lexeme in separators:
                token_type = "separator"
            elif lexeme in operators:
                token_type = "operator"
            elif lexeme in literals:
                token_type = "literal"

        if token_type is not None:
            tokens.append((token_type, lexeme))

    return tokens



# to run the lexer and output into a file. 
tokens = lexer('input_scode.txt')
with open("output.txt", "w") as outfile:
    for token in tokens:
        outfile.write(token[0] + ": " + token[1] + "\n")
