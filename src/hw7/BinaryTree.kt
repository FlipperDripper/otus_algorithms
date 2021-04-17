package tarasov.outs.trees

open class BinaryTree {
    var root: Node? = null
        private set

    fun insert(value: Int) {
        root = insert(root, value)
    }

    protected open fun insert(node: Node?, key: Int): Node? {
        if (node == null) {
            return Node(key)
        }
        if (key == node.key) {
            return node
        }
        if (key < node.key) {
            node.left = insert(node.left, key)
        } else {
            node.right = insert(node.right, key)
        }
        return node
    }

    fun remove(key: Int) {
        root = remove(root, key)
    }

    protected open fun remove(node: Node?, key: Int): Node? {
        if (node == null) {
            return null
        }
        if (key == node.key) {
            if (node.left == null && node.right == null) {
                return null
            }
            if (node.left == null) {
                return node.right
            }
            if (node.right == null) {
                return node.left
            }
            val smallestValue = findSmallestValue(node.right!!)
            node.key = smallestValue
            node.right = remove(node.right, smallestValue)
            return node
        }
        if (key < node.key) {
            node.left = remove(node.left, key)
        } else {
            node.right = remove(node.right, key)
        }
        return node
    }

    private fun findSmallestValue(node: Node): Int {
        return if (node.left == null) node.key else findSmallestValue(node.left!!)
    }

    fun search(value: Int): Boolean {
        return search(root, value)
    }

    private fun search(node: Node?, key: Int): Boolean {
        if (node == null) {
            return false
        }
        if (key == node.key) {
            return true
        }
        return if (key < node.key) search(node.left, key) else search(node.right, key)
    }
}