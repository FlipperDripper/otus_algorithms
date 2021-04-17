package tarasov.otus.sort

import java.io.RandomAccessFile
import java.nio.file.Files
import java.nio.file.Path
import java.io.File

class MergeSort {
    private val bufferSize = 8192

    fun sort(file: File?) {
        RandomAccessFile(file, "rw").use { accessFile -> sort(0, accessFile.length() / 2 - 1, accessFile) }
    }

    private fun sort(left: Long, right: Long, file: RandomAccessFile) {
        if (left >= right) {
            return
        }
        if (right - left < bufferSize) {
            innerSort(left, right, file)
            return
        }
        val pivot = (left + right) / 2
        sort(left, pivot, file)
        sort(pivot + 1, right, file)
        merge(left, pivot, right, file)
    }

    private fun innerSort(left: Long, right: Long, file: RandomAccessFile) {
        val array = IntArray((right - left).toInt() + 1)
        file.seek(left * 2)
        for (i in array.indices) {
            array[i] = file.readUnsignedShort()
        }
        QuickSort().sort(array)
        file.seek(left * 2)
        for (value in array) {
            file.writeShort(value)
        }
    }

    private fun merge(left: Long, pivot: Long, right: Long, file: RandomAccessFile) {
        var l = left
        var r = pivot + 1
        val mergeFilename = "$left.$pivot.$right"
        RandomAccessFile(mergeFilename, "rw").use { mergeFile ->
            while (l <= pivot && r <= right) {
                file.seek(l * 2)
                val leftItem = file.readUnsignedShort()
                file.seek(r * 2)
                val rightItem = file.readUnsignedShort()
                if (leftItem < rightItem) {
                    mergeFile.writeShort(leftItem)
                    l++
                } else {
                    mergeFile.writeShort(rightItem)
                    r++
                }
            }
            while (l <= pivot) {
                file.seek(l++ * 2)
                mergeFile.writeShort(file.readUnsignedShort())
            }
            while (r <= right) {
                file.seek(r++ * 2)
                mergeFile.writeShort(file.readUnsignedShort())
            }
            for (i in left..right) {
                file.seek(i * 2)
                mergeFile.seek((i - left) * 2)
                file.writeShort(mergeFile.readUnsignedShort())
            }
        }
        Files.deleteIfExists(Path.of(mergeFilename))
    }
}