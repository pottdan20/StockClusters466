"""
Stores sectors for each ticker, to be used when analyzing clusters 
"""
from matplotlib import pyplot as plt

"""
Looks at data points in each cluster based on sector
"""
class ClusterAnalysis: 
    def __init__(self, cluster_file, sectors_file): 
        self.cluster_file = cluster_file # Result of k-means
        self.sectors_file = sectors_file # All tickers and their corresponding sector
        self.sectors = {} # Key = ticker, Value = sector
    
    
    """
    Stores all tickers in dictionary self.sectors
    """
    def store_tickers_by_sector(self): 
        in_file = open(self.sectors_file, "r")
        keep_going = True 
        curr_sector = ""
        while(keep_going): 
            line = in_file.readline()
            if line == '': # EOF
                keep_going = False 
            elif line.split()[0].strip() == "SECTOR": 
                curr_sector = line[6:].strip()
            else: 
                ticker = line.strip()
                self.sectors[ticker] = curr_sector
        in_file.close()
    
    
    """
    Looks at sectors within each cluster 
    Displays each cluster as a pie chart of sectors 
    """
    def get_cluster_sectors(self): 
        # Each cluster is stored as a dictionary, where each dictionary has: 
        #       key = sector str 
        #       value = number of data points with that sector
        curr_cluster_sectors = {"CLUSTER: 1": {}, 
                                "CLUSTER: 2": {}, 
                                "CLUSTER: 3": {}, 
                                "CLUSTER: 4": {}}
        # Read the file and store sectors for each cluster 
        in_file = open(self.cluster_file, "r")
        curr_cluster = ""
        for line in in_file: 
            if line.split(":")[0] == "CLUSTER": 
                curr_cluster = line.strip()
            else: 
                ticker = line.strip()
                # Get Counts 
                try: # Use try, except since some points do not have a sector (OTHER)
                    sector = self.sectors[ticker]
                    if sector not in curr_cluster_sectors[curr_cluster]:
                        curr_cluster_sectors[curr_cluster][sector] = 1 
                    else: 
                        curr_cluster_sectors[curr_cluster][sector] += 1                    
                except: 
                    if "OTHER" not in curr_cluster_sectors[curr_cluster]: 
                        curr_cluster_sectors[curr_cluster]["OTHER"] = 1
                        pass
                    else: 
                        pass
                        curr_cluster_sectors[curr_cluster]["OTHER"] += 1   
        # Display each cluster as a pie chart, where data is number of points in each sector
        for cluster in curr_cluster_sectors: 
            sectors = []
            counts = []
            for sector in curr_cluster_sectors[cluster]:                 
                counts.append(curr_cluster_sectors[cluster][sector])
                sectors.append(sector + " " + str(curr_cluster_sectors[cluster][sector]))
            plt.rcParams["figure.figsize"] = [7.50, 3.50]
            plt.rcParams["figure.autolayout"] = True
            colors = ["#71f79f", "#3dd6d0", "#15b097", "#513c2c", "#28190e", "#4f000b", "#720026", "#ce4257", "#ff7f51", "#ff9b54", "#4b4e6d"]
            patches = plt.pie(counts, colors=colors, shadow=True, startangle=90)
            plt.legend(patches, sectors, loc="best")
            plt.axis('equal')
            plt.title(cluster)
            plt.show()
            
            
"""
Looks at sector distribution within each cluster
"""
def main(): 
    my_analizer = ClusterAnalysis("resulting_clusters.txt", "sectors.txt")
    my_analizer.store_tickers_by_sector()
    my_analizer.get_cluster_sectors()
            
if __name__ == "__main__":    
    main()