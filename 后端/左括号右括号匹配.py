# **3.栈的算法题："(","<","{","[",")",">","}","]",在左右括号中，判断输入的字符括号是否左右匹配并打印结果。**

left = ["(", "<", "{", "["]
right = [")", ">", "}", "]"]


def func(spe):
    if spe == ")":
        return "("
    elif spe == ">":
        return "<"
    elif spe == "}":
        return "{"
    elif spe == "]":
        return "["
    else:
        return "ERROR"


def main(str):
    lis, r = [], 0
    str = list(str.strip())
    for i in str:
        if i in left:
            lis.append(i)
        elif i in right:
            if lis and len(lis) > 0:
                spe = func(i)
                if spe == lis[-1]:
                    lis.pop()
                    r += 1
                else:
                    r = -1
                    break
            else:
                r = -1
                break
        else:
            print("此字符不是括号字符")
            break

    if r == -1:
        print("括号不匹配",lis)
    else:
        if lis:
            print("左括号多余", lis)
        else:
            print("匹配完成共有%s对括号" % r)

if __name__ == "__main__":
    while True:
        try:
            main(input())
        except:
            break