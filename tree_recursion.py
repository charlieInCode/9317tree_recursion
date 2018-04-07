# Tree recursion. Question taken from UNSW COMP9318 lab1.

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

t = Tree('*', [Tree('1'),
               Tree('2'),
               Tree('+', [Tree('3'),
                          Tree('4')])])

def print_tree(root, indent=0):
    print(' ' * indent, root)
    if len(root.children) > 0:
        for child in root.children:
            print_tree(child, indent+4)

def myfind(s, char):
    pos = s.find(char)
    if pos == -1:  # not found
        return len(s) + 1
    else:
        return pos

def next_tok(s):  # returns tok, rest_s
    if s == '':
        return (None, None)
    # normal cases
    poss = [myfind(s, ' '), myfind(s, '['), myfind(s, ']')]
    min_pos = min(poss)
    if poss[0] == min_pos:  # separator is a space
        tok, rest_s = s[: min_pos], s[min_pos + 1:]  # skip the space
        if tok == '':  # more than 1 space
            return next_tok(rest_s)
        else:
            return (tok, rest_s)
    else:  # separator is a [ or ]
        tok, rest_s = s[: min_pos], s[min_pos:]
        if tok == '':  # the next char is [ or ]
            return (rest_s[:1], rest_s[1:])
        else:
            return (tok, rest_s)

def str_to_tokens(str_tree):
    # remove \n first
    str_tree = str_tree.replace('\n', '')
    out = []

    tok, s = next_tok(str_tree)
    while tok is not None:
        out.append(tok)
        tok, s = next_tok(s)
    return out

def make_tree(tokens):
    # first need to change the list of chars to a stack
    # can print the stack to see what it is.
    stack = list()
    while tokens:
        if tokens[-1] == '[':
            tokens.pop()
            t = list()
            while stack[-1] != ']':
                t.append(stack.pop())
            stack.pop()
            tokens.append(t)
        else:
            t = list()
            t = tokens.pop()
            stack.append(t)

    stack.reverse()

    # using recursion.
    root = Tree(stack[0])
    child = stack[1:]
    def f(root, child):
        if len(child) == 1:
            if isinstance(child[-1],list):
                return f(root, child[-1])
        for i in range(len(child)):
            if isinstance(child[i], list):
                f(root.children[-1], child[i])
            else:
                root.add_child(Tree(child[i]))
        return root
    return f(root, child)

# can also get the max depth of tree by using recursion.
def max_depth(root):
    while root:
        depth = 1
        if root.children is not None:
            max_d_children = 0
            for i in root.children:
                if max_depth(i) > max_d_children:
                    max_d_children= max_depth(i)
            depth = 1 + max_d_children

        return depth



if __name__ == '__main__':
    print('A model tree below')
    print_tree(t)
    print('-'*120)

    print('A str_tree transfers to a list of some chars')
    # format: node, list-of-children
    str_tree = '''
    1 [2 [3 4       5          ] 
       6 [7 8 [9]   10 [11 12] ] 
       13
      ]
    '''
    toks = str_to_tokens(str_tree)
    print(toks)
    print('-'*120)

    print('A list of some chars transfer to a model tree.')
    tt = make_tree(toks)
    print_tree(tt)