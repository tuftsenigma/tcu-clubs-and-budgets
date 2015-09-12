
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


'''
source: http://oco-carbon.com/metrics/find-pareto-frontiers-in-python/
Method to take two equally-sized lists and return just the elements which lie 
on the Pareto frontier, sorted into order.
Default behaviour is to find the maximum for both X and Y, but the option is
available to specify maxX = False or maxY = False to find the minimum for either
or both of the parameters.
'''
def pareto_frontier(Xs, Ys, maxX = True, maxY = True):
# Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
# Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]    
# Loop through the sorted list
    for pair in myList[1:]:
        if maxY: 
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y...
                p_front.append(pair) # ...and add them to the Pareto frontier
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y...
                p_front.append(pair)
# Turn resulting pairs back into a list of Xs and Ys
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]
    return p_frontX, p_frontY



if __name__ == '__main__':

    plt.rc("font", family="serif")
    with open("../data/funds_vs_followers.json", "r") as f:
        club_data = json.load(f)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    followers =  [club_data[club]["followers"] for club in club_data.keys()]
    funds = [club_data[club]["funds"] for club in club_data.keys()]

    # scatter plot
    plt.scatter(followers, funds)

    # pareto frontier
    pf = pareto_frontier(followers, funds)
    plt.plot(pf[0], pf[1])
    plt.xlim([0,1500])
    plt.ylim([0,480000])

    # labels
    plt.xlabel(r"$Followers$")
    plt.ylabel(r"$Funds$")

    for xy in zip(followers, funds):
        for club in club_data.keys():
            if club_data[club]["followers"] == xy[0] and club_data[club]["funds"] == xy[1]:
                this_club = club
        ax.annotate(this_club, 
            xy=xy, 
            verticalalignment='left',
            horizontalalignment='left',
            rotation=45)

    plt.show()


