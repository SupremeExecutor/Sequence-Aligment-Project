import sys

def main():
    input = sys.argv[1]
    output = sys.argv[2]

    file = open(input, "r")
    lines = file.readlines()
    str1 = lines[0].strip()
    n1 = []
    str2 = ""
    n2 = []
    parseStr2 = False
    for l in lines[1:]:
        l = l.strip()
        if l.isalpha():
            str2 = l
            parseStr2 = True
            continue
        if parseStr2:
            n2.append(int(l))
        else:
            n1.append(int(l))
    # print("str1: ", str1)
    # print(n1)
    # print(generateStr(str1, n1))
    # print("str2: ", str2)
    # print(n2)
    # print(generateStr(str2, n2))
    return 0

def generateStr(str, n):
    for i in n:
        str = str[:i+1]+str+str[i+1:]
    return str

if __name__=="__main__": 
    main() 