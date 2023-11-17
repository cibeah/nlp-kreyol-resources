
Extraction script
#TODO: look for source in translation
#TODO: Only take sentences with upper case character at the start


Notes on further corrections done with the `check_dataset()` function:

**Fix bad Text/Author/Source/Translation Identification**
* 200, 225, 577, 762, 1006, 1154, 1285, 1523, 1529, 2079, 2146, 2155, 2254, 2282, 2576, 2963, 3040, 3215, 3291, 3398, 3347, 3463, 3470, 3497, 3925, 4016, 4059, 4094, 4123, 4153, 4278, 4465, 4492, 4496, 4566, 4683, 4703, 4735, 4820, 4832, 4846, 4918

**Keep literal translations of idiomatic expressions only**
* 170, 538, 683, 726, 766, 1184, 2284, 2624, 4174, 4444

**Not a sentence pair. Deleted or replaced by word pair**
* 39, 930, 1580, 4381, 

**Removed additional comment made by author**
* 935, 1232, 1373, 3810,

**Others**
* Remove `ttm` abbreviation, but keep the corresponding sentence pairs
* Clean `.` at the beginning
* Check all lines starting with ^[A-Z] to check for truncated sentences, or misaligned
* Handle special characters (°)

Remove "ttm"