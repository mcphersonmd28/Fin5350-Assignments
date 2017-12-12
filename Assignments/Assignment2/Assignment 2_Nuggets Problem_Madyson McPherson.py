def is_nugget_number(candidate, small=6, medium=9, large=20):
    for i in range(candidate//small + 1):
        for j in range(candidate//medium + 1):
            for k in range(candidate//large +1):
                if(small*i + medium*j + large*k == candidate):
                    return True
                
    
    return False

def main():
    small, medium, large = 6, 9, 20
    count = 0
    largest = small - 1
    candidate = small
    
    while count != small:
        if(is_nugget_number(candidate)):
            count += 1
        else:
            largest = candidate
            count = 0
        candidate += 1
        
    print("The largest number of nuggets you cannot buy is: {0}".format(largest))

main()
