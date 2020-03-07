import numpy as np
import utils



def linear_UCB(data):

    num_patients = len(data)
    num_features = 20

    regret = 0
    num_correct = 0
    arms = ["low", "medium", "high"]

    true_vals = list(data["Therapeutic Dose of Warfarin"])
    for i in range(len(true_vals)):
        if true_vals[i] < 21:
            true_vals[i] = "low"
        elif true_vals[i] > 49:
            true_vals[i] = "high"
        else:
            true_vals[i] = "medium"
    A_map = {}
    b_map = {}
    p_map = {}
    for arm in arms:
        A_map[arm] = np.identity(num_features)
        b_map[arm] = np.zeros(num_features)

    for t in range(num_patients):
        for arm in arms:
            theta = np.matmul(np.linalg.inv(A_map[arm]), b_map[arm])
            features = utils.extractFeatures(data, t)
            p_map[arm] = np.matmul(theta.T, features) + np.sqrt(np.matmul(np.matmul(features.T, np.linalg.inv(A_map[arm])), features))
        best_arm = max(p_map, key=lambda k: p_map[k])
        if best_arm == true_vals[t]:
            num_correct +=1
        A_map[best_arm] += np.outer(features, features)
        r = 0 if best_arm == true_vals[t] else -1
        regret -= r
        b_map[best_arm] +=r * features

    accuracy = num_correct * 1.0 / num_patients
    print("Accuracy: ", accuracy)
    print("Inaccuracy: ", 1 - accuracy)
    print("Regret: ",regret)

data = utils.sampleKRows()
linear_UCB(data)