#The computer guesses my number

def print_header():
    print("\tWelcome to 'Guess My Number'!")
    print("\tI'm thinking of a number between 1 and 100.")
    print("\tGive the computer hints with 'higher' and 'lower'")
    print("\tOnce the guess is right, type 'correct'")
    print("\tTry to guess it in as few attempts as possible.\n")

def print_footer(guess, tries):
    print("You guessed it!  The number was", guess)
    print("And it only took", tries, "tries!\n")
    print("\n\nPress the enter key to exit.")

def response(answer):
    input("Was this guess too high or too low?")

'''    
def too_high(answer):
    print("Is the guess too high?") 
    answer = input("Let the computer know.")
    print("Your guess is too high.")
    print("\n\nTry again!")
    
def too_low(answer):
    print("Is the guess too low?")
    answer = input("Let the computer know.")
    print("Your guess is too low.")
    print("\n\nTry again!")
'''   
def main():#code goes here!
    #print the header
    print_header()
    
    #set the inital values
    low = 0
    upper = 100
    guess = int((upper + low)/2)
    tries = 1
    answer = input(guess)
    done = False
    #the loo
    while done != True:
        if answer == "higher":
            low = guess
            guess = int((upper+low)/2)
            answer = input(guess)
        elif answer == "lower":
            upper = guess
            guess = int((upper+low)/2)
            answer = input(guess)
        elif answer == "correct":
            done = True
        tries +=1
    
    print_footer(guess, tries)
    print("The computer's guess is", guess, ". It's correct!")
        
    
if __name__ == "__main__":
    main()