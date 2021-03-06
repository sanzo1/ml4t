"""
A simple wrapper for RT
"""

import numpy as np
import random as rd

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.verbose = verbose
        self.leaf_size = leaf_size
        pass  # move along, these aren't the drones you're looking for

    def addEvidence(self, X, Y):
        def built_tree(dataX, dataY):
            leaf =- 1000
            # checks if the data points in a branch has equal or less than the leaf size
            if dataX.shape[0] <= self.leaf_size:
                # average the Y's  of data points in a leaf
                self.tree = np.asarray([[leaf, np.mean(dataY), np.nan, np.nan]])
                return self.tree
            elif len(set(dataY)) == 1:
                # checks if all the Y values are the same, then just return Y
                self.tree = np.asarray([[leaf, np.mean(dataY), np.nan, np.nan]])
                return self.tree
            else:
                # randomly order the features in a list
                randomList = rd.sample(xrange(0, dataX.shape[1]), dataX.shape[1])
                i = randomList[0]  # select the first feature in the list to split on
                z = 1
                # check if the feature has any information,
                # if all data points in that feature is the same pick another feature
                while len(set(dataX[:, i])) == 1 and z <= dataX.shape[1]:
                    i = randomList[z]
                    z += 1
                # if selected feature has all the same values then make it a leaf and return the mean of the data points
                if len(set(dataX[:, i])) == 1:
                    return [[leaf,np.mean(dataY), np.nan, np.nan]]
                else:
                    # if selected feature has information, find two data points to split on
                    SplitVal = np.mean(np.random.choice(dataX[:, i], size=2, replace=False))
                    # if split value is greater than all data points you need
                    # to select another split value to prevent the right branch from being blank
                    while SplitVal == np.amax(dataX[:, i]):
                        SplitVal = np.mean(np.random.choice(dataX[:, i], size=2, replace=False))
                    a=dataX[:, i] <= SplitVal  # data on the left
                    dataxl = dataX[a]
                    datayl = dataY[a]
                    leftTree = built_tree(dataxl, datayl)  # recursively build the left tree
                    dataxr = dataX[~a]  # data on the right
                    datayr = dataY[~a]
                    rightTree = built_tree(dataxr, datayr)  # recursively build the right tree
                    root = [i, SplitVal, 1, len(leftTree)+1]
                    self.tree = np.vstack((root, leftTree, rightTree))
                    return self.tree
        return built_tree(X, Y)

    def query(self, points):
        i = 0
        sh = points.shape[0]
        result = np.empty([sh])  # create an empty array
        while i < sh:
            arrayIndex = 0
            while ~np.isnan(self.tree[arrayIndex, 3]):  # checks if the row in "decision tree" array is a leaf
                val = self.tree[arrayIndex, 1]  # finds the split value
                # compares the split value of the feature with the value of the same feature in test set
                if points[i, int(self.tree[arrayIndex, 0])] <= val:
                    arrayIndex += 1  # goes to the right tree
                else:
                    arrayIndex += int(self.tree[arrayIndex, 3])  # goes to the left tree
            value = self.tree[arrayIndex, 1]
            result[i] = value
            i += 1
        return result

#if __name__=="__main__":
#    print "the secret clue is 'zzyzx'"