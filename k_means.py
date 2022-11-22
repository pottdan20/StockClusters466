import math 
import random 
from matplotlib import pyplot as plt
#plt.style.use('seaborn-whitegrid')
import numpy as np


class DataPoint: 
    def __init__(self, ticker, percent, volatility): 
        self.ticker = ticker 
        self.percent = percent 
        self.volatility = volatility 
        self.cluster = None
        self.p_zScore = None
        self.v_zScore = None

    

    def __repr__(self):
        return '(' + self.ticker + ', ' + str(round(self.percent, 3)) + ', ' + str(round(self.volatility, 3)) + ', ' + str(self.cluster) + ')'

    def __eq__(self, other): 
        return type(other) == DataPoint and \
            self.ticker == other.ticker and \
                self.percent == other.percent and \
                    self.volatility == other.volatility                      

class Clusterer: 
    def __init__(self, k, in_file): 
        self.k = k
        self.training_data = []
        self.centers = [None for i in range(0, k)] # Index is cluster number, value is data point of center  
        self.percentMean = None
        self.volatilityMean = None 
        self.percentSD = None
        self.volatilitySD = None     
        self.read_data(in_file)
        self.set_standanrd_deviations()
        self.set_point_zScores()
        
    def set_point_zScores(self):
        for point in self.training_data:
            point.p_zScore = (point.percent - self.percentMean)/self.percentSD
            point.v_zScore = (point.volatility - self.volatilityMean) / self.volatilitySD
    
    def set_standanrd_deviations(self): #sets the standard deviation for percent and volatility
        percentDiffSum = 0
        volatilityDiffSum = 0
        count = 0
        for point in self.training_data:
            count += 1
            percentDiffSum += (point.percent - self.percentMean) ** 2
            tempVDiff = (point.volatility - self.volatilityMean) ** 2
            if not math.isnan(tempVDiff):
                volatilityDiffSum += tempVDiff
        self.percentSD = math.sqrt(percentDiffSum / (count -1))
        self.volatilitySD = math.sqrt(volatilityDiffSum / (count -1))


    def print_zScores(self):
        for i in range (0,100):
            p = self.training_data[i]
            print(p.ticker + "    p_zScore: " + str(p.p_zScore)   )     
             

    # Reads data file into a list of DataPoint objects
    
    def read_data(self, in_file): 
        data_file = open(in_file, 'r')
        percentSum = 0
        volatilitySum = 0
        count = 0
        for line in data_file: 
            line_lst = line.split(" ")
            self.training_data.append(DataPoint(line_lst[0], float(line_lst[1]), float(line_lst[2])))
            percentSum += float(line_lst[1])
            tempV = float(line_lst[2])
            if not math.isnan(tempV):
                volatilitySum += tempV

            count += 1

        self.percentMean = percentSum / count
        self.volatilityMean = volatilitySum / count
        print(volatilitySum)
        data_file.close()

    # Generates k random centers in range of the training data min and max 
    def initialize_centers(self): 
        min_percent = self.training_data[0].percent
        max_percent = self.training_data[0].percent
        min_volatility = self.training_data[0].volatility
        max_volatility = self.training_data[0].volatility
        # Find the min and max for percent and volatility in training data 
        for point in self.training_data:
            if point.percent < min_percent:
                min_percent = point.percent 
            if point.percent > max_percent: 
                max_percent = point.percent 
            if point.volatility < min_volatility: 
                min_volatility = point.volatility 
            if point.volatility > max_volatility: 
                max_volatility = point.volatility
        # Create random centers 
        for i in range(0, self.k):
            name = "CENTER_" + str(i)
            percent = random.randint(int(min_percent), int(max_percent))
            volatility = random.randint(int(min_volatility), int(max_volatility))
            p_zScore = (percent - self.percentMean)/self.percentSD
            v_zScore = (volatility - self.volatilityMean) / self.volatilitySD
            to_add = DataPoint(name, percent, volatility)
            to_add.p_zScore = (percent - self.percentMean)/self.percentSD
            to_add.v_zScore = (volatility - self.volatilityMean)/self.volatilitySD
            self.centers[i] = to_add

        
        '''for i in range(0, self.k): 
            name = "CENTER_" + str(i)
            index = random.randint(0, len(self.training_data))
            percent = self.training_data[index].percent   
            volatility = self.training_data[index].volatility
            self.centers[i] = DataPoint(name, percent, volatility)'''
        
    def assign_to_cluster(self, data_point): 
        # Look at the distance to each cluster center and keep track of minimum 
        min_dist = float('inf')
        min_cluster = 0 
        for i in range(0, len(self.centers)): 
            curr_cluster_center = self.centers[i] 
            # Use Euclidean distance metric 
            curr_dist = math.pow((curr_cluster_center.p_zScore - data_point.p_zScore), 2) + \
                math.pow((curr_cluster_center.v_zScore - data_point.v_zScore), 2)
            if curr_dist < min_dist: 
                min_dist = curr_dist
                min_cluster = i 
        # Assign data point to the closest cluster
        data_point.cluster = min_cluster 
    
    def adjust_centers(self): #with z-scores
        done_clustering = False  
        percent_sums = [0 for x in range(0, len(self.centers))]
        volatility_sums = [0 for x in range(0, (len(self.centers)))]
        counts = [0 for x in range(0, len(self.centers))]                
        for data_point in self.training_data: 
            percent_sums[data_point.cluster] += data_point.percent 
            volatility_sums[data_point.cluster] += data_point.volatility 
            counts[data_point.cluster] += 1
        for cluster_number in range(0, len(self.centers)):             
            if counts[cluster_number] != 0: 
                percent_mean = percent_sums[cluster_number] / counts[cluster_number]
                volatility_mean = volatility_sums[cluster_number] / counts[cluster_number]
                if self.centers[cluster_number].percent == percent_mean and \
                    self.centers[cluster_number].volatility == volatility_mean: 
                    done_clustering = True 
                else: 
                    done_clustering = False
                    self.centers[cluster_number].percent = percent_mean 
                    self.centers[cluster_number].volatility = volatility_mean
                    self.centers[cluster_number].p_zScore = (percent_mean - self.percentMean)/self.percentSD
                    self.centers[cluster_number].v_zScore = (volatility_mean - self.volatilityMean)/self.volatilitySD
        return done_clustering 
      
    def adjust_centers_without_sd(self): #this was original functionality before we clustered by zScores
        done_clustering = False  
        percent_sums = [0 for x in range(0, len(self.centers))]
        volatility_sums = [0 for x in range(0, (len(self.centers)))]
        counts = [0 for x in range(0, len(self.centers))]                
        for data_point in self.training_data: 
            percent_sums[data_point.cluster] += data_point.percent 
            volatility_sums[data_point.cluster] += data_point.volatility 
            counts[data_point.cluster] += 1
        for cluster_number in range(0, len(self.centers)):             
            if counts[cluster_number] != 0: 
                percent_mean = percent_sums[cluster_number] / counts[cluster_number]
                volatility_mean = volatility_sums[cluster_number] / counts[cluster_number]
                #print(str(cluster_number) + " " + str(percent_mean) + " " + str(volatility_mean))
                if self.centers[cluster_number].percent == percent_mean and \
                    self.centers[cluster_number].volatility == volatility_mean: 
                    done_clustering = True 
                else: 
                    done_clustering = False
                    self.centers[cluster_number].percent = percent_mean 
                    self.centers[cluster_number].volatility = volatility_mean
        return done_clustering 
    

    def cluster(self):  
        keep_going = True 
        
        
        while keep_going:
            for data_point in self.training_data: 
                self.assign_to_cluster(data_point)
            if self.adjust_centers() == True: 
                keep_going = False
        
        '''colors = ["red", "green", "blue", "pink", "purple", "orange", "yellow", "grey"]
        clusters = {}
        for data_point in self.training_data:
            if data_point.cluster not in clusters: 
                clusters[data_point.cluster] = []
            clusters[data_point.cluster].append(data_point)
        for cluster in clusters: 
            data_points = clusters[cluster]
            p = []
            v = []            
            for data_point in data_points: 
                p.append(data_point.percent)
                v.append(data_point.volatility)
            plt.scatter(p, v, color = colors[data_point.cluster], alpha = 0.5)            
        centersp = []
        centersv = []
        for center in self.centers: 
            centersp.append(center.percent)
            centersv.append(center.volatility)
        plt.scatter(centersp, centersv, color = "black", alpha = 0.5)            
        plt.show()    '''    

            
            



          
            
            


def main(): 
    my_clusterer = Clusterer(7, "testfile.txt")
    my_clusterer.initialize_centers()   
    my_clusterer.cluster()

   
    '''for data_point in my_clusterer.training_data:
        if data_point.cluster not in clusters: 
            clusters[data_point.cluster] = []
        clusters[data_point.cluster].append(data_point)
    
    for cluster in clusters: 
        data_points = clusters[cluster]
        p = []
        v = []
        hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        print(hexadecimal)
        for data_point in data_points: 
            p.append(data_point.percent)
            v.append(data_point.volatility)
        plt.scatter(p, v, color = hexadecimal, alpha = 0.5)
    plt.show()'''

    colors = ["red", "green", "blue", "pink", "purple", "orange", "yellow", "grey"]
    clusters = {}
    for data_point in my_clusterer.training_data:
        if data_point.cluster not in clusters: 
            clusters[data_point.cluster] = []
        clusters[data_point.cluster].append(data_point)
    for cluster in clusters: 
        data_points = clusters[cluster]
        p = []
        v = []            
        for data_point in data_points: 
            p.append(data_point.percent)
            v.append(data_point.volatility)
        plt.scatter(p, v, color = colors[data_point.cluster], alpha = 0.5)            
    centersp = []
    centersv = []
    for center in my_clusterer.centers: 
        centersp.append(center.percent)
        centersv.append(center.volatility)
    plt.scatter(centersp, centersv, color = "black", alpha = 0.5)            
    plt.show()        

        



    my_clusterer.cluster()
    
if __name__ == "__main__":    
    main()