## Image Duplicate Script
Program to detect and delete duplicated images using image hashes.

### Requirements
- <i>imagehash</i> package
- <i>send2trash</i> package
- <i>Pillow</i> package

### NB:
- <i>IMAGE_DIRECTORY</i> will have to be replaced by your own directory.
- Duplicate files are not deleted permanently, but are sent to the recycle bin via the <i>send2trash</i> package.
- <i>Elapsed_time</i> is the time taken for the image comparisons and not the time taken the whole program to run.
- Some <i>variables</i> and <i>print</i> statements are commented becuase they are only used for debugging purposes.

#### PS:
- Script is still under development and there are some bugs that prevent deletion of multiple duplicates at once.
(meaning program will have to be run multiple times to delete more than 2 duplicates. But this is not a major problem
as <b>binary search</b> is used for better comparison time.)
- In the list displaying the output for duplicate files:
    - If file is displayed  before the separator (' '), it means that is the duplicate and that's what is deleted later
     in the code.
    - More files appearing together before the separator(' ') in the list means more duplicates, and can be deleted
     safely as there will still be <b>one</b> copy of the image left.