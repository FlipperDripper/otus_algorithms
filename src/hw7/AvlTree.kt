package tarasov.outs.trees

class AvlTree : BinaryTree() {
    override fun insert(node: Node?, key: Int): Node? {
        val unbalanced = super.insert(node, key)
        return rebalance(unbalanced)
    }

    override fun remove(node: Node?, key: Int): Node? {
        val unbalanced = super.remove(node, key)
        return rebalance(unbalanced)
    }

    private fun smallLeftRotation(y: Node?): Node? {
        val x = y!!.right
        val z = x!!.left
        x.left = y
        y.right = z
        recalculateHeight(y)
        recalculateHeight(x)
        return x
    }

    private fun rebalance(node: Node?): Node? {
        var node = node
        recalculateHeight(node)
        val balance = getBalance(node)
        if (balance > 1) {
            node = if (getHeight(node!!.right!!.left) < getHeight(node.right!!.right)) smallLeftRotation(node) else bigLeftRotation(node)
        } else if (balance < -1) {
            node = if (getHeight(node!!.left!!.right) < getHeight(node.left!!.left)) smallRightRotation(node) else bigRightRotation(node)
        }
        return node
    }

    private fun smallRightRotation(y: Node?): Node? {
        val x = y!!.left
        val z = x!!.right
        x.right = y
        y.left = z
        recalculateHeight(y)
        recalculateHeight(x)
        return x
    }

    private fun bigLeftRotation(node: Node?): Node? {
        node!!.right = smallRightRotation(node.right)
        return smallLeftRotation(node)
    }

    private fun bigRightRotation(node: Node?): Node? {
        node!!.left = smallLeftRotation(node.left)
        return smallRightRotation(node)
    }

    private fun getHeight(node: Node?): Int {
        return node?.height ?: 0
    }

    private fun getBalance(node: Node?): Int {
        return if (node == null) 0 else getHeight(node.right) - getHeight(node.left)
    }

    private fun recalculateHeight(node: Node?) {
        if (node != null) {
            node.height = Math.max(getHeight(node.left), getHeight(node.right)) + 1
        }
    }
}