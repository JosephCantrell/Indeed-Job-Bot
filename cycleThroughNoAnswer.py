import csv

listOfQuestions = []

listOfAnsweredJobs = []

print('S to skip, E to Exit')

with open('noAnswers.txt', 'r') as csvfile: 
    for line in csvfile.readlines():
        if 'No Answer:' in line:
            listOfQuestions.append(line)
            
for line in listOfQuestions:
    skip = False
    # Compare the list of answered questions against our current question to see if we have answered it yet
    for answered in listOfAnsweredJobs:
        if line in answered:
            print('Upcoming quesiton is a duplicate. Skipping')
            skip = True
            break
    if not skip:
        print(line)
        answer = input("Enter the answer: ")
        if answer == 'e' or answer == 'E':
            print('Quitting')
            break
        elif answer == 's' or answer == 'S':
            print('Skipping question.')
        else:
            temp = line.split(': ')
            
            temp = temp[1]
            
            temp = temp[:-4]
            
            file = open('Answers.txt','a')
            file.write("'" + temp + "',")
            file.write("'" + str(answer) + "',\n")
            file.close()
        listOfAnsweredJobs.append(line)