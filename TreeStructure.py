# 树结构
from collections import defaultdict

Tree = lambda: defaultdict(Tree)

tree = Tree()

tree['pets']['dog'] = 1
tree['fruits']['pear'] = 20
tree['fruits']['apple'] = 10
tree['pets']['cat'] = 3

# 树的第一层有两个分支
tree.keys()
#dict_keys(['fruits', 'pets'])

# fruits子树下有两个节点
tree['fruits'].items()
#dict_items([('apple', 10), ('pear', 20)])
