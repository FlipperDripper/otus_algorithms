package tarasov.outs.trees

class Node(var key: Int) {
	var left: Node? = null
	var right: Node? = null
	var height = 0
	var priority = 0
}