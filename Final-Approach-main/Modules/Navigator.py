'''
Final Approach v1.0
Lydia, Dylan, Robel
Dec 2, 2022
SWE II
'''

from subprocess import call
import subprocess

class LaunchModule():
    def __init__(self) -> None:
        pass
    
    # Launch Modules
    def mod_breakCSV(self):
        call(['Python3', r'Modules\breakCSV.py'])

    def mod_main_parser(self):
        call(['Python3', r'Modules\main_parser.py'])

    def mod_UserSelect(self):
       call(['Python3', r'Modules\UserSelect.py'])

    

if __name__ == "__main__":
    Launch = LaunchModule()

    #! Break Day CSV into flights 
    
    # Launch GUI to allow selection of Data from Partition Data
    Launch.mod_UserSelect()

    # Parse Data of Selected Items
    Launch.mod_main_parser()

    #! Graph Calculated Values