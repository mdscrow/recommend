from math import sqrt,acos,degrees

def parse_history() -> list:
    """
    creates the history table from the history file

    returns a list of customer vectors

    python starts from 0 whereas the data starts from 1, data should be subtracted by 1 excluding the header 
    
    indexes go [item][customer] unlike the data so 0 and 1 when being read are flipped
    
    ☠ live laugh luffy ☠
    """
    history = open("history.txt", "r")
    header = history.readline()
    header_info = list(map(int,header.split()))
    history_table = []
    for i in range(header_info[1]):
        history_table.append([])
        for j in range(header_info[0]):
            history_table[i].append(0)
    for _ in range(header_info[2]):
        purchase_data = list(map(int,history.readline().split()))
        history_table[purchase_data[1]-1][purchase_data[0]-1] = 1
    history.close()
    return history_table

def count_positives(history_table) -> int:
    """counts all of the positives in the history table"""
    sum = 0
    for item in history_table:
        for customer in item:
            sum += customer
    return sum

def precalc_angles(history_table) -> list:
    """
    returns a 2d list with every pairwise angle in degrees
    """
    angle_matrix = []
    for i in range(len(history_table)):
        angle_matrix.append([])
        for j in range(len(history_table[0])):
            if i == j: #ignores self pairs
                angle_matrix[i].append(-1)
            else:
                angle_matrix[i].append(get_angle(history_table[i],history_table[j]))
    return angle_matrix

def pick_best_angle(angles,banned_indecies) -> list:
    """
    takes a 1d list of angles and picks the lowest unless the lowest >= 90 or banned or itself
    """
    lowest_index = -1
    lowest_angle = 90
    for angle_index in range(len(angles)):
        if angles[angle_index] < lowest_angle and angle_index+1 not in banned_indecies and angles[angle_index] != -1:
            lowest_angle = angles[angle_index]
            lowest_index = angle_index + 1
        
    return [lowest_index,lowest_angle]
        
def calculate_average(angle_matrix) -> float:
    denominator = len(angle_matrix)**2 - len(angle_matrix)
    numerator = 0
    for x in angle_matrix:
        for y in x:
            if y != -1:
                numerator += y
    return round(numerator/denominator,2)

def get_angle(avector, bvector) -> float:
    dp = dot_product(avector,bvector)
    angle = acos(dp/(magnitude(avector)*magnitude(bvector)))
    return round(degrees(angle),2)


def magnitude(vector) -> float:
    sum_of_squares = 0
    for value in vector:
        sum_of_squares += value**2
    return sqrt(sum_of_squares)
    

def dot_product(a, b) -> int:
    dp = 0
    for i in range(len(a)):
        dp += a[i]*b[i]
    return dp

def main() -> None:
    ht = parse_history()
    queries = open("queries.txt", "r").read().split("\n")
    am = precalc_angles(ht)
    print(f'Positive entries: {count_positives(ht)}')
    print(f'Average angle: {calculate_average(am):.2f}') # :.2f AND rounding in the functions so that 0 or 1 dp get lengthened, but <3 dp get rounded instead of truncated
    for query in queries:
        if len(query) > 0:
            banned_indecies = list(map(int,query.split()))
            recs = []
            print(f'Shopping cart: {query}')
            for item in query.split(): 
                rec = pick_best_angle(am[int(item)-1],banned_indecies)
                if rec[0] == -1: #if no recommended angle
                    print(f'Item: {item} no match')
                else:
                    if rec[0] not in recs:
                        recs.append(rec[0])
                    print(f'Item: {item}; match: {rec[0]}; angle: {rec[1]:.2f}')
            print(f'Recommend: {" ".join(list(map(str,recs)))}')

if __name__ == "__main__":
    main()
