package tarasov.otus.sort


class QuickSort {
    fun sort(array: IntArray) {
        sort(0, array.size - 1, array)
    }

    fun sort(left: Int, right: Int, array: IntArray) {
        if (left >= right) {
            return
        }
        val center = partition(left, right, array)
        sort(left, center - 1, array)
        sort(center + 1, right, array)
    }

    fun partition(left: Int, right: Int, array: IntArray): Int {
        val pivot = array[right]
        var a = left - 1
        for (m in left..right) {
            if (array[m] <= pivot) {
                swap(++a, m, array)
            }
        }
        return a
    }

    fun swap(from: Int, to: Int, array: IntArray) {
        val buffer = array[from]
        array[from] = array[to]
        array[to] = buffer
    }
}