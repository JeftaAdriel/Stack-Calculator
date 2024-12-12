def level(char):
    if char == "^":
        return 3
    elif char == "/" or char == "*":
        return 2
    elif char == "+" or char == "-":
        return 1
    else:
        return 0
