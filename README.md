# Badge-Generator
A simple tool generating badges for conferences or similar

## What you need
* python3
* psnup
* pdf2ps
* ps2pdf
* pyx (you need this patched version for some coloring) --- https://github.com/Spyrko/pyx

## How to use
call with: python3 badges.py [input.csv] [args]   

| Argument      | Description                                           |
|:------------- |:----------------------------------------------------- |
| -c            | Print cutting-lines (no effect if no -m is specified) |
| -h            | Print this help                                       |
| -m [count]    | Multiple badges per page                              |
| -n [count]    | Create multiple badges per entry                      |
| -o [filename] | Set output file (without .pdf)                        |
| -p [profile]  | Profile to use                                        |

## Input
The csv must have the following shape:  
**Name;Handle;Organization;ID**  
You can escape characters for csv import by **\\**  
Note that you might need some additional escapes for LaTeX

## Profiles
You can edit or add profiles in profiles.py  
Make sure you add your profile to the dict and the default profile is a valid key of that dict
