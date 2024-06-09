class Word:
    def __init__(self, indonesian, sundanese):
        self.indonesian = indonesian.lower()
        self.sundanese = sundanese.lower()
        
class BSTNode:
    def __init__(self, word, key):
        self.word = word
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, key):
        key = key.lower()
        if self.root is None:
            self.root = BSTNode(word, key)
        else:
            self._insert(self.root, word, key)

    def _insert(self, node, word, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(word, key)
            else:
                self._insert(node.left, word, key)
        else:
            if node.right is None:
                node.right = BSTNode(word, key)
            else:
                self._insert(node.right, word, key)

    def search(self, term):
        term = term.lower()
        return self._search(self.root, term)

    def _search(self, node, term):
        if node is None or node.key == term:
            return node
        if term < node.key:
            return self._search(node.left, term)
        return self._search(node.right, term)

    def search_contains(self, substring):
        substring = substring.lower()
        results = []
        self._search_contains(self.root, substring, results)
        return results

    def _search_contains(self, node, substring, results):
        if node is not None:
            if substring in node.key:
                results.append(node.word)
            self._search_contains(node.left, substring, results)
            self._search_contains(node.right, substring, results)

    def delete(self, key):
        self.root = self._delete(self.root, key.lower())

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.word = temp.word
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order_traversal(self):
        words = []
        self._in_order_traversal(self.root, words)
        return words

    def _in_order_traversal(self, node, words):
        if node:
            self._in_order_traversal(node.left, words)
            words.append(node.word)
            self._in_order_traversal(node.right, words)

bst_indonesian = BST()
bst_sundanese = BST()

initial_words = [
    {"indonesian": "Makan", "sundanese": "Neda"},
    {"indonesian": "Minum", "sundanese": "Inum"},
    {"indonesian": "Tidur", "sundanese": "Sare"},
    {"indonesian": "Berjalan", "sundanese": "Lalampahan"},
    {"indonesian": "Duduk", "sundanese": "Diuk"},
    {"indonesian": "Buku", "sundanese": "Buku"},
    {"indonesian": "Rumah", "sundanese": "Imah"},
    {"indonesian": "Anak", "sundanese": "Budak"},
    {"indonesian": "Air", "sundanese": "Cai"},
    {"indonesian": "Api", "sundanese": "Seuneu"}
]

for word in initial_words:
    word_obj = Word(word["indonesian"], word["sundanese"])
    bst_indonesian.insert(word_obj, word["indonesian"])
    bst_sundanese.insert(word_obj, word["sundanese"])
