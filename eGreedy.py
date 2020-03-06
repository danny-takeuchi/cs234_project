
def calc_egreedy_u(sold_not_sold, h):
    n = len(sold_not_sold)
    p = np.asarray([(w + 1)/ (w + l + 2) for w,l in sold_not_sold])
    best_arm = np.argmax(p)
    result = np.random.choice(["greedy","not_greedy"], p = [e, 1 - e])
    if result == "greedy":

    else:

    return

h = 10
import time
start_t = time.time()
print(calc_max_u(sold_not_sold, h))
print("Runtime: " + str(time.time() - start_t))
print(calc_expected_u(sold_not_sold, h))
# print(calc_egreedy_u(sold_not_sold, h))