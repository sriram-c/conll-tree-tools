#Function to return index of a value from a list
#Written by Roja(04-12-19)
####################################################
p_lst = [0,1,0,0,2,3,6,4,5,8,9,4,17,18,19,11,14,11,16,0,0,1,11,12,13]

def return_index(lst, val):
    index = []
    for i in range(len(lst)):
        if val == lst[i]:
            index.append(i)
    return(index)        

#To test uncomment below step
#print(return_index(p_lst, 4))
