# 常用排序算法

def bubble_sort(nums):
    """
    冒泡排序，最坏时间复杂度O(n^2)
    :param nums: 待排序数列
    :return: 排好序的数列
    """
    for i in range(len(nums) - 1):
        # 已排好序的部分不用再次遍历
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


def selection_sort(nums):
    """
    选择排序，时间复杂度O(n^2)
    :param nums:待排序的数列
    :return: 排好序的数列
    """
    for i in range(len(nums) - 1):
        minIndex = i
        for j in range(i + 1, len(nums)):
            # 更新最小值索引
            if nums[j] < nums[minIndex]:
                minIndex = j
        nums[i], nums[minIndex] = nums[minIndex], nums[i]
    return nums


def insertion_sort(nums):
    """
    插入排序
    :param nums:待排序数列
    :return: 排好序的数列
    """
    for i in range(len(nums)):
        # 保存当前待插入数的值和位置
        cursor = nums[i]
        pos = i

        while pos > 0 and nums[pos - 1] > cursor:
            # 比待插入数大的元素后移
            nums[pos] = nums[pos - 1]
            pos = pos - 1

        nums[pos] = cursor
    return nums


def shell_sort(nums):
    """
    希尔排序
    :param nums: 待排序的数列
    :return: 排好序的数列
    """
    gap = len(nums) // 2
    while gap > 0:
        for i in range(gap, len(nums)):
            cursor = nums[i]
            pos = i
            # 比较gap的两头，如果左边的比右边的大就互换位置
            while pos > 0 and nums[pos - gap] > cursor:
                nums[pos] = nums[pos - gap]
                pos = pos - gap
            nums[pos] = cursor
        # gap取半，直到gap=0，整个循环结束，当gap=1的时候，即最后一轮就和插入排序一样了。
        gap = gap // 2

    return nums


def merge_sort(nums):
    """
    归并排序
    :param nums:待排序的数列
    :return: 排好序的数列
    """

    # left， right是已排好序的两个子序列
    def merge(left, right):
        # 保存归并后的结果
        result = []
        # i: 左序列的游标， j: 右序列的游标
        i = j = 0
        while i < len(left) and j < len(right):
            # 比较左右序列游标所指的值，较小的那个被取出放入result中，且该序列游标右移
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # 剩余的元素直接添加到末尾
        result = result + left[i:] + right[j:]
        return result

    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    return merge(left, right)


def quick_sort(nums):
    # 选取第一个元素作为基准数
    return qsort(nums, 0, len(nums) - 1)


def qsort(nums, left, right):
    """
    快速排序函数
    :param nums: 待排序数组
    :param left: 待排序的左边界
    :param right: 待排序的右边界
    :return: 排好序的数列
    """
    if left >= right:
        return nums
    key = nums[left]  # 取最左边的为基准数
    lp = left  # 左指针
    rp = right  # 右指针
    while lp < rp:
        # 分区过程，将比基准数大的放到右边，小于或等于它的数都放到左边
        while nums[rp] >= key and lp < rp:
            # rp所指的数值大于基数，即右边的数保持不动，
            # 指针继续左移直到所指的数小于基数或者和左指针重合
            rp -= 1
        while nums[lp] <= key and lp < rp:
            # lp所指的数值小于基数，即左边的数保持不动，
            # 指针右移直到所指的数大于基数或者和右指针重合
            lp += 1

        # 左指针和右指针所指的数值交换，这样满足比基准数大的放到右边，小于或等于它的数都放到左边
        nums[lp], nums[rp] = nums[rp], nums[lp]

    # 将基数和lp所指的数交换位置
    nums[left], nums[lp] = nums[lp], nums[left]

    # 递归过程，分解更小的组
    qsort(nums, left, lp - 1)
    qsort(nums, rp + 1, right)

    return nums


def heap_sort(nums):
    """
    堆排序
    :param nums: 待排序的数列
    :return: 排好序的数列
    """
    n = len(nums)
    # 最后一个非叶子节点
    first = int(n / 2 - 1)
    # 构造最大堆，自下而上
    for start in range(first, -1, -1):
        max_heapify(nums, start, n - 1)
    # 堆排，将最大堆转换成有序数组
    for end in range(n - 1, 0, -1):
        nums[end], nums[0] = nums[0], nums[end]
        max_heapify(nums, 0, end - 1)
    return nums


def max_heapify(ary, start, end):
    """
    最大堆调整，将堆的末端子节点作调整，使得子节点永远小于父节点
    :param ary:待调整的数列
    :param start:当前需要调整最大堆的位置
    :param end:调整边界
    :return: 调整后的数列
    """
    root = start
    while True:
        child = root * 2 + 1
        if child > end:
            break
        # 取较大的子节点
        if child + 1 <= end and ary[child] < ary[child + 1]:
            child = child + 1
        # 较大的子节点成为父节点
        if ary[root] < ary[child]:
            ary[root], ary[child] = ary[child], ary[root]
            root = child
        else:
            break


if __name__ == "__main__":
    nums = [7, 5, 2, 3, 1]
    # print(bubble_sort(nums))
    # print(selection_sort(nums))
    # print(insertion_sort(nums))
    # print(shell_sort(nums))
    # print(merge_sort(nums))
    # print(quick_sort(nums))
    print(heap_sort(nums))