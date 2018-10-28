#----------------------------------------------------------------------------------------
# This file defines alternate CC/note numbers that the controls in this script should use.
# Please note the following:

# --> Do not change the spacing or punctuation in this file.
# --> Do not change the name of this file.
# --> Do not use a CC or note number on a particular channel more than once.
# --> The channel that controls use is determined in the DDC Editor.
# --> The type of MIDI message (CC/note) that buttons use is determined in the DDC Editor.
#----------------------------------------------------------------------------------------


""" The CC numbers to use for encoder groups A-D. """
ENC_GROUP_NUMS = ((56, 57, 58, 59, 60, 61, 62, 63),             # Group A : Encoders
                  (8, 9, 10, 11, 12, 13, 14, 15),      # Group B : Knobs
                  (16, 17, 18, 19, 20, 21, 22, 23),     # Group C : Faders
                  (80, 81, 82, 83, 84, 85, 86, 87))     # Group D : Not Used

""" Whether or not encoder group A uses pitch bend messages on ch1 - 8.
If this is set to True, the CC#s for Group A above are ignored. """
ENC_GROUP_A_PB = False

""" Whether or not encoder group B uses pitch bend messages on ch9 - 16.
If this is set to True, the CC#s for Group B above are ignored. """
ENC_GROUP_B_PB = False

""" The note (or CC) numbers to use for button groups A-D. """
BTN_GROUP_NUMS = ((24, 25, 26, 27, 28, 29, 30, 31),     # Group A : Buttons Left 1st Row
                  (32, 33, 34, 35, 36, 37, 38, 39),     # Group B : Buttons Left 2nd Row
                  (40, 41, 42, 43, 44, 45, 46, 47),     # Group C : Buttons Right 1st Row
                  (48, 49, 50, 51, 52, 53, 54, 55))     # Group D : Buttons Right 2nd Row

""" The note (or CC) number to use for the lock button. """
LOCK_BTN_NUM = 88  # Not Used

""" The note (or CC) numbers to use for the direct page buttons. """
DIRECT_PAGE_BTN_NUMS = (80, 81, 82, 83, 84, 85, 86, 87) # those are notes and note cc causing side effects (36, 37, 38, 39, 40, 41, 42, 43)

""" The note (or CC) number to use for the previous page button. """
PREV_PAGE_BTN_NUM = 89  # Not Used

""" The note (or CC) number to use for the next page button. """
NEXT_PAGE_BTN_NUM = 90  # Not Used
