import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径
from Stack import ArrayStack
from HashMap import HashMapOpenAddressing as HashMap


def ParenthesesChecker(brakets: str) -> bool:
    '''检查左右括号是否匹配'''
    stack: ArrayStack = ArrayStack()
    match: HashMap = HashMap()
    left_brakets: str = '([{'
    right_brakets: str = ')]}'
    for i, j in zip(left_brakets, right_brakets):
        match[ord(i)] = j
    for i in brakets:
        if i in left_brakets:
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
        print(i, ParenthesesChecker(brakets=i))