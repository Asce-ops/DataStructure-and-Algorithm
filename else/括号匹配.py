import sys
from pathlib import Path

sys.path.append(str(object=Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径
from Stack import ArrayStack
from HashMap import HashMapOpenAddressing as HashMap


def ParenthesesChecker(brackets: str) -> bool:
    '''检查左右括号是否匹配'''
    stack: ArrayStack = ArrayStack()
    match: HashMap = HashMap()
    left_brackets: str = '([{'
    right_brackets: str = ')]}'
    for i, j in zip(left_brackets, right_brackets):
        match[ord(i)] = j
    for i in brackets:
        if i in left_brackets:
            stack.push(item=i)
        else:
            if len(stack) == 0:
                return False
            else:
                if match[ord(stack.peek())] == i:
                    stack.pop()
                else:
                    return False
    return True if len(stack) == 0 else False



if __name__ == '__main__':
    test: list[str] = [
        '{{([][])}()}',
        '[[{{(())}}]]',
        '[][][](){}',
        '([)]',
        '((()]))',
        '[{()]'
    ]
    for i in test:
        print(i, ParenthesesChecker(brackets=i))