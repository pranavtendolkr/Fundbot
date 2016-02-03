import json
import matplotlib
import math
import collections
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from collections import OrderedDict

plt.axis('off')
matplotlib.use('Agg')

class PlotGraph(object):

    @staticmethod
    def plot_graph(data=None):
        jsonresp=json.loads(str(data))
        
        anchors=jsonresp['resolution']['map']['anchors']
        anchor_polygon=[]
        for anchor in anchors:
            PlotGraph.draw_anchor_points(anchor)
            anchor_polygon.append([anchor['position']['x'],anchor['position']['y']])
        PlotGraph.draw_polygon(anchor_polygon)
        
        top5nodes=PlotGraph.top_five(jsonresp)
        
        for node in top5nodes:
            PlotGraph.draw_node_points(node)

    @staticmethod
    def draw_anchor_points(anchor=None):
        plt.plot(anchor['position']['x'],anchor['position']['y'],'ro')
        plt.text(anchor['position']['x'],anchor['position']['y'],anchor['name'])
        print anchor['position']['x'],anchor['position']['y'], anchor['name']
        plt.savefig('myfig')
        plt.show()
    
    @staticmethod
    def draw_polygon(anchor_polygon=None):
        plt.axes()
        polygon = plt.Polygon(anchor_polygon,fill=None)
        plt.gca().add_patch(polygon)
        plt.savefig('myfig')
        plt.show()
        
    @staticmethod
    def draw_node_points(anchor=None):
        plt.plot(anchor['coordinates']['x'],anchor['coordinates']['y'],'g^')
        plt.savefig('myfig')
        plt.show()
    
    
    @staticmethod
    def top_five(jsonresp=None):
        anchors=jsonresp['resolution']['map']['anchors']
        anchor_polygon=[]
        for anchor in anchors:
            anchor_polygon.append([anchor['position']['x'],anchor['position']['y']])
        polygon = Polygon(anchor_polygon)
        polygon.centroid
        centroid=polygon.centroid.wkt
        centroid=centroid[centroid.find('(')+1: centroid.find(')')+1]
        x_center=float(centroid[(centroid.find('(')+1):centroid.find(' ')].strip(' \t\n\r'))
        y_center=float(centroid[centroid.find(' '):centroid.find(')')].strip(' \t\n\r'))
        nodes=jsonresp['resolution']['map']['nodes']        
        new_dict={}
        for node in nodes:
             x2=node['coordinates']['x']
             y2=node['coordinates']['y']
             dist = math.hypot(x2 - x_center, y2 - y_center)
             new_dict[dist]=node
        ordered= OrderedDict(sorted(new_dict.items(), key=lambda t: t[0]))
        #print ordered
        top5=[]
        for i,tuple in enumerate(ordered.items()):
            top5.append(tuple[1])
            if(i>4):
                break
        return top5
        
with open('data.json', 'r') as content_file:
    content = content_file.read()

#print content
PlotGraph.plot_graph(str(content))
