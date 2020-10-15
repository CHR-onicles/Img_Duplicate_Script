import imagehash
from PIL import Image
import os
import time
import send2trash
import shutil


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


start = time.time()

IMAGE_DIRECTORY = 'B:\\Desktop\\Img_Duplicate_Script'
# IMAGE_DIRECTORY = 'B:\\Desktop\\Wallpapers'
# IMAGE_DIRECTORY = 'B:\\Desktop\\R_wallpapers'
# os.mkdir('B:\\Desktop\\Corrupt_Pics')
# CORRUPT_PICS_DIRECTORY = 'B:\\Desktop\\Corrupt_Pics'
os.chdir(IMAGE_DIRECTORY)

# Only add picture files to pic_list
pic_list = list()
for files in os.listdir():
    if '.jpg' in files or '.png' in files:
        pic_list.append(files)

pic_hashes = list()  # for referral to actual pics using indices
sorted_pic_hashes = list()  # for efficient binary search
duplicates = list()

# duplicate_set_count = 0

#                     if duplicate_counter >= 1 and item2 == pic_list[-1]:
#                         duplicates.append(item1)
#                         duplicates.append(' ')  # to separate sets of duplicates
#                         duplicate_set_count += 1
#                         break
#                 elif (img1_hash != img2_hash) and duplicate_counter > 0 and item2 == pic_list[-1]:
#                     duplicates.append(item1)
#                     duplicates.append(' ')
#                     duplicate_set_count += 1

# main  CODE starts here
# add keyboard Interrupt exception in case it takes too long
for pic in pic_list:
    img_hash = imagehash.average_hash(Image.open(pic))
    pic_hashes.append(str(img_hash))  # have to convert to str for sort() operation
sorted_pic_hashes = pic_hashes.copy()  # making shallow copy to prevent deletion in one list from affecting the other
sorted_pic_hashes.sort()

pop_count = -1
c_counter = 0

for count, h in enumerate(pic_hashes):
    value = binary_search(sorted_pic_hashes, 0, len(sorted_pic_hashes) - 1, h)
    print(f'Loop count: {count + 1}')
    if value == -1:
        continue
    else:
        while value != -1:
            value = binary_search(sorted_pic_hashes, 0, len(sorted_pic_hashes) - 1, h)
            c_counter += 1
            print(f'Comparison count: {c_counter}')

            if value != -1:
                sorted_pic_hashes.remove(sorted_pic_hashes[value])
                pop_count += 1

            if pop_count >= 1:  # ignoring itself, there is another similar hash (duplicate image)
                if pop_count >= 1 and value != -1:
                    duplicates.append(pic_list[count])

                elif pop_count >= 1 and value == -1:
                    pop_count = -1
                    duplicates.append(' ')
                    break

            if value == -1:
                pop_count = -1


stop = time.time()

if len(duplicates) > 0:
    print(f'\n{duplicates}')

    # d_count = 0
    # inner_count = 0
    # delete_list = list()

    # for count, item in enumerate(duplicates):
    #     if item != ' ':
    #         d_count += 1
    #     else:
    #         for i in range(1, d_count):
    #             inner_count += 1
    #             if duplicates[(count - d_count) + inner_count] != ' ':
    #                 delete_list.append(duplicates[(count - d_count) + inner_count])
    #         d_count = 0
    #         inner_count = 0

    choice = input('Extra duplicates will be transferred to recycle bin.\n'
                   'Do you wish to proceed?: [y/n]  ')

    if choice[0].lower() == 'y':
        for files in duplicates:
            if files != ' ':
                send2trash.send2trash(files)
        print('\nAll extra duplicate files deleted successfully!')
    else:
        print('\nOperation Cancelled...')

else:
    print('\nThere are no image duplicates!')


elapsed_time = stop - start
print(f'\nElapsed time: {round(elapsed_time, 2)} seconds')
