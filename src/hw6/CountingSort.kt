package tarasov.otus.sort

import java.io.File
import java.io.RandomAccessFile

class CountingSort {
    private val bufferSize = 65536

    fun sort(inputFile: File, outputFile: File?) {
        val sums = LongArray(bufferSize.toInt())
        RandomAccessFile(inputFile, "r").use { accessInputFile ->
            while (accessInputFile.filePointer < inputFile.length()) {
                sums[accessInputFile.readUnsignedShort()] = sums[accessInputFile.readUnsignedShort()] + 1
            }
            for (i in 1 until sums.size) {
                sums[i] = sums[i] + sums[i - 1]
            }
            RandomAccessFile(outputFile, "rw").use { accessOutputFile ->
                var position = inputFile.length() - 2
                while (position >= 0) {
                    accessInputFile.seek(position)
                    val number = accessInputFile.readUnsignedShort()
                    sums[number] = sums[number] - 1
                    accessOutputFile.seek(sums[number] shl 1)
                    accessOutputFile.writeShort(number)
                    position -= 2
                }
            }
        }
    }
}