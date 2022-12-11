# Reads calculated data from pickle and plots values to graph
import matplotlib.pyplot as plt
import numpy as np
import re, datetime
from datetime import date
from message import popUpError

# Class represents data Extracted from one CSV File
class entity:
    def __init__(self, fileName:str, avg_speed:dict, coordinates:dict) -> None:
        self.fileName = fileName
        self.avg_speed = avg_speed
        self.coordinates = coordinates

# Maps and Displays Entities to Graph
class graph_mapper:
    def __init__(self, entities:object) -> None:
        self.entities = entities
        
    def main(self) -> None:
        '''Plot Entity Data'''
        # Zip FileName with values and apply label
        for val, name in zip([i.avg_speed for i in self.entities], [i.fileName for i in self.entities]):
            x_pnt = [j for j in val.keys()]
            y_pnt = [k for k in val.values()]

            plt.plot(x_pnt, y_pnt, marker = 'o', label = f'{self.legend_generator(name)}')

        # Apply Graph Customizations
        self.decorate()
        plt.show()


    def legend_generator(self, pathName) -> str:
        '''Extracts Date from CSV File Name'''
        
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', pathName)
        time_match = re.search(r'\d{2}_\d{2}_\d{2}', pathName)
        date_label = datetime.datetime.strptime(date_match.group(), '%Y-%m-%d').date()
        try:
            time_label = datetime.datetime.strptime(time_match.group(), '%H_%M_%S').time()
        except:
            time_label = ':)'
            
        return f'{date_label}, {time_label}'

    def decorate(self):
        '''Apply Decoration to Graph'''
       
        # # Plt Attributes
        plt.legend()
        plt.yticks((40,50,60,70,80))

        font1 = {'family':'serif','color':'green','size':12}
        font2 = {'family':'serif','color':'green','size':12}
        font3 = {'family':'serif','color':'green','size':16}
        plt.title("Average Speed Graph", fontdict=font3, loc='center')
        plt.xlabel("Altitude (ft.)", fontdict=font1)
        plt.ylabel('Speed (Knts.)', fontdict=font2)

        # Grid Properties
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

    if __name__ == "__main__":
        main()