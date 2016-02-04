import json
import matplotlib
matplotlib.use('Agg')
import math
import collections
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from collections import OrderedDict
from random import randint

plt.axis('off')
height=12
length=14
imagepath="/tmp/%s" % randint(0,100) + "results"

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
        problem=jsonresp['problem']
        for node in top5nodes:
            PlotGraph.draw_node_points(node,problem)

        return PlotGraph.upload_image(imagepath)

    @staticmethod
    def upload_image(path=None):
        import pyimgur
        #PATH = "image.jpg"
        client_id = '3ae9387ee3ea12f'
        im = pyimgur.Imgur(client_id)
        uploaded_image = im.upload_image(path+".png", title="Mutual fund graph")
        return uploaded_image.link

    @staticmethod
    def draw_anchor_points(anchor=None):
        plt.plot(anchor['position']['x'],anchor['position']['y'],'ro')
        plt.text(anchor['position']['x'],anchor['position']['y'],anchor['name'])
        #print anchor['position']['x'],anchor['position']['y'], anchor['name']
        figure = plt.gcf()
        figure.set_size_inches(length,height)
        plt.axis('scaled')
        plt.savefig(imagepath,dpi=100)
        plt.show()

    @staticmethod
    def draw_polygon(anchor_polygon=None):
        plt.axes()
        polygon = plt.Polygon(anchor_polygon,fill=True,color='#4863A0',closed=True)
        plt.gca().add_patch(polygon)
        figure = plt.gcf()
        figure.set_size_inches(length,height)
        plt.axis('scaled')
        plt.savefig(imagepath,dp=100)
        plt.show()

    @staticmethod
    def draw_node_points(anchor=None,problem=None):
        plt.plot(anchor['coordinates']['x'],anchor['coordinates']['y'],'g^')
        node_label_solref=anchor["solution_refs"]
        all_ref=""
        problems=problem["options"]
        for sol_ref in node_label_solref:
            solution_label=filter(lambda problem: problem['key'] == sol_ref, problems)
            if all_ref=="":
                all_ref=all_ref+solution_label[0]["name"]
            else:
                all_ref=all_ref+","+solution_label[0]["name"]
        plt.text(anchor['coordinates']['x'],anchor['coordinates']['y'],all_ref)
        plt.axis('scaled')
        figure = plt.gcf()
        figure.set_size_inches(length,height)
        plt.savefig(imagepath,dp=100)
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
            print "i=%s" % i
            top5.append(tuple[1])
            if(i>=4):
                break
        return top5

# with open('x.json', 'r') as content_file:
#     content = content_file.read()
#
# #print content
# PlotGraph.plot_graph(str(content))
