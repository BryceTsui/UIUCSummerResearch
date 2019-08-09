import os
import sys

# Instructions:
        # go into each  then count dirs with c source code
        # then go into each dir submission
        # get c source code into string
        # count how many source code


# We start at problems directory
directory = 'G:\\UIUC\iterate\problems'
# Checksum path
path = 'G:\\UIUC\iterate\problems\checksum'

for filename in os.listdir(directory):
    # We don't want to include iterate into this
    if filename.endswith(".py"):
        continue
    # We want to CD to checksum
    if os.path.isdir(filename):
        print(os.path.abspath(filename))
        problemDir = os.path.abspath(filename)
        cwd = os.getcwd()
        os.chdir(problemDir)
        print(os.listdir(problemDir))
        stdDirs = os.listdir(problemDir)
        # count directories -- count students
        # Initialize count
        count = 0
        # If we are in the problems directory
        if os.path.isdir(problemDir):
            # for directory in students,
            for dir in stdDirs:
                # if directory starts with period, continue because we don't want to go into those
                # Directories that start with "." dion't contain C programs we can print
                if (dir.startswith(".")):
                    continue
                # other directories would be students
                if (os.path.isdir(dir)):
                    # for every student found, increment
                    count =+ 1
                    # cd into these directories

                    # print current path, to know where we are at
                    print(os.path.abspath(dir))
                    # ***To this point we are inside a student directory
                    submission = os.path.abspath(dir)
                    os.chdir(dir)
                    # Need to cd into attemptsssssss - MAJOR KEY
                    # stops working here, got to cd into attempts, there is different attempts per student
                    # these attempts all contain different C code and fixes
                    if (os.path.isdir(submission)):
                        for direct in os.listdir(submission):
                            # the attempts directory starts with 0
                            # if we see a 0, we want to go into that directory
                            if direct.startswith("0"):
                                print("direct!")
                                print(os.path.abspath(direct))
                                # change directory
                                #os.chdir(direct)
                                # print current path

                                # store that path
                                attempts = os.path.abspath(direct)
                                # trying to CD into attempts
                                os.chdir(attempts)
                                for filename in os.listdir(attempts):
                                # if the file ends with c in submissions, we want to print
                                    if filename.endswith(".c"):
                                        print(os.path.abspath(filename))
                                        lineList = list()
                                        fileName = filename
                                        with open(fileName) as f:
                                            lineList = f.readlines()
                                        # here we print the source code
                                        for l in lineList:
                                            print(l)
                                            continue
                                    else:
                                        continue
            # print number of student submissions
            print("Number of students:", count)
            # print where we are at
            print(os.path.abspath(filename))
        os.chdir(cwd)
        print (os.listdir(cwd))





    # IGNORE
    # Now we are inside checksum
    # Inside checksum, print number of students, then cd into each student submission
    """ for filename in os.listdir(path):
        # print number of students
        print(filename)
        # cd into each students directory
        os.chdir(filename)
        # if the file ends with .c, print each line as list
        if filename.endswith(".c"):
            lineList = list()
            fileName = filename
            with open(fileName) as f:
                lineList = f.readlines()
            for l in lineList:
                print(l)
            continue
        else:
            continue """