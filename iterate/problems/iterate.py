import os
import sys

# We start at problems directory
directory = '/Users/Adelson/documents/iterate/problems'
# Checksum path
path = '/Users/Adelson/documents/iterate/problems/checksum'

for filename in os.listdir(directory):
    # We don't want to include iterate into this
    if filename.endswith(".py"):
        continue
    # We want to CD to checksum
    if os.path.isdir(filename):
        print(os.path.abspath(filename))
        problemDir = os.path.abspath(filename)
        cwd = os.getcwd()
        # join paths
        problem_path = os.path.join(cwd, problemDir)
        print(os.listdir(problem_path))
        # lists the directories
        stdDirs = os.listdir(problem_path)
        # count directories -- count students
        # Initialize count
        count = 0
        # If we are in the problems directory
        if os.path.isdir(problem_path):
            # for directory in students,
            for d in stdDirs:
                # if directory starts with period, continue
                if (d.startswith(".")):
                    continue
                submission_path = os.path.join(problem_path, d)
                # other directories would be students
                if (os.path.isdir(submission_path)):
                    # for every student found, increment
                    count = + 1
                    if (os.path.isdir(submission_path)):
                        for direct in os.listdir(submission_path):
                            # we want to keep joining the paths to go further into the directories
                            file_path = os.path.join(submission_path, direct)
                            if direct.startswith("0"):
                                for filename in os.listdir(file_path):
                                    # if the file ends with c in submissions, we want to print
                                    if filename.endswith(".c"):
                                        print(os.path.abspath(filename))
                                        lineList = list()
                                        fileName = os.path.join(
                                            file_path, filename)
                                        with open(fileName) as f:
                                            lineList = f.readlines()
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
        print(os.listdir(cwd))
