import imagehash
from PIL import Image
import os
import time
import send2trash
import shutil


start = time.time()

IMAGE_DIRECTORY = 'B:\\Desktop\\R_wallpapers'
os.mkdir('B:\\Desktop\\Corrupt_Pics')
CORRUPT_PICS_DIRECTORY = 'B:\\Desktop\\Corrupt_Pics'
os.chdir(IMAGE_DIRECTORY)

# Only add picture files to pic_list
pic_list = list()
for files in os.listdir():
    if '.jpg' in files or '.png' in files:
        pic_list.append(files)

duplicates = list()

num_of_loops = 0
num_of_comparisons = 0
duplicate_set_count = 0


for item1 in pic_list:
    num_of_loops += 1
    print(f'Number of loops: {num_of_loops}')
    if item1 not in duplicates:
        img1 = Image.open(item1)
        try:
            img1_hash = imagehash.average_hash(img1)
        except FileNotFoundError:
            pass
        except OSError:
            print(item1)
            shutil.move(IMAGE_DIRECTORY + '\\' + item1, CORRUPT_PICS_DIRECTORY + '\\' + item1)
        duplicate_counter = 0

        for item2 in pic_list:
            num_of_comparisons += 1
            print(f'Number of comparisons: {num_of_comparisons}')
            if item2 != item1:
                img2 = Image.open(item2)
                try:
                    img2_hash = imagehash.average_hash(img2)
                except FileNotFoundError:
                    pass
                except OSError:
                    print(item2)
                    shutil.move(IMAGE_DIRECTORY + '\\' + item2, CORRUPT_PICS_DIRECTORY + '\\' + item2)

                if img1_hash == img2_hash:
                    duplicate_counter += 1
                    duplicates.append(item2)

                    if duplicate_counter >= 1 and item2 == pic_list[-1]:
                        duplicates.append(item1)
                        duplicates.append(' ')  # to separate sets of duplicates
                        duplicate_set_count += 1
                        break
                elif (img1_hash != img2_hash) and duplicate_counter > 0 and item2 == pic_list[-1]:
                    duplicates.append(item1)
                    duplicates.append(' ')
                    duplicate_set_count += 1


stop = time.time()

if len(duplicates) > 0:
    print(f'\nThere are {duplicate_set_count} set(s) of duplicates:')
    print(f'\n{duplicates}')

    d_count = 0
    inner_count = 0
    delete_list = list()

    for count, item in enumerate(duplicates):
        if item != ' ':
            d_count += 1
        else:
            for i in range(1, d_count):
                inner_count += 1
                if duplicates[(count - d_count) + inner_count] != ' ':  # to make sure it doesn't append the spaces
                    delete_list.append(duplicates[(count - d_count) + inner_count])
            d_count = 0
            inner_count = 0

    print(f'\nDuplicates to be deleted: ')
    print(f'\n {delete_list}')

    choice = input('Extra duplicates will be transferred to recycle bin.\n'
                   'Do you wish to proceed?: [y/n]  ')

    if choice[0].lower() == 'y':
        for files in delete_list:
            send2trash.send2trash(files)
        print('\nAll extra duplicate files deleted successfully!')
    else:
        print('\nOperation Cancelled...')

else:
    print('\nThere are no image duplicates!')


elapsed_time = stop - start
print(f'\nElapsed time: {round(elapsed_time, 2)} seconds')
