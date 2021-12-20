import numpy as np

surround_mask = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [0, 0, 0]], np.int8)
surround_mask=surround_mask[surround_mask!=0
]
tree_arr=[1,2,3,4,5,6]
surround_labels=[2,5,6]
min_surround_label=2
print(surround_labels != min_surround_label)
print(surround_labels[surround_labels != min_surround_label])#得到第一个不等于min_label的值
tree_arr[surround_labels[surround_labels != min_surround_label]] = min_surround_label
print(tree_arr)