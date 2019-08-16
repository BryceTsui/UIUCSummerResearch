import os
import subprocess
import json
def exe_command(work_path,command):

    """
    execute command in the terminal

    Parameters
    ----------
    work_path: str
        The path that you want to execute this command

    command: str
        The command you want to execute
    Returns
    -------
    None
    """
    #save the original dir then we can change to the original dir after executing command
    original_cwd = os.getcwd()
    #print(original_cwd)
    os.chdir(work_path)
    # output = subprocess.getstatusoutput('clang checksum.c')
    # print(output)
    output = subprocess.getstatusoutput(command)
    os.chdir(original_cwd)
    return output

def getAllResult(problems_path,whitebox_path,blackbox_path):

    standardOutouts_whitebox = []
    standardOutouts_blackbox = []

    #the number of test cases in whitebox and blackbox
    N_White = 10
    N_Black = 6

    for i in range(1, N_White+1):
        # if your Os is Linux, you need to change a.exe -> ./a.out.
        out_path =  whitebox_path + str(i) + ".out"
        with open(out_path,'r') as out_file:
            standardOutput = out_file.read()
            standardOutput = standardOutput.strip()
        standardOutouts_whitebox.append(standardOutput)


    for i in range(1, N_Black+1):
        # if your Os is Linux, you need to change a.exe -> ./a.out.
        out_path = blackbox_path + str(i) + ".out"
        with open(out_path,'r') as out_file:
            standardOutput = out_file.read()
            standardOutput = standardOutput.strip()
        standardOutouts_blackbox.append(standardOutput)


    for i in standardOutouts_whitebox:
        print(i)

    for i in standardOutouts_blackbox:
        print(i)

    print(len(standardOutouts_whitebox))
    print(len(standardOutouts_blackbox))

    all_result_white = {}
    all_result_black = {}

    for problem in os.listdir(problems_path):

        problem_path = os.path.join(problems_path, problem)

        if os.path.isdir(problem_path):
            # print("problem"+problem)
            for student_dir in os.listdir(problem_path):
                # print(student_dir)

                student_dir_path = os.path.join(problem_path, student_dir)
                if os.path.isdir(student_dir_path) and student_dir != 'tests' :
                    # print("student:"+student_dir)

                    for submit_dir in os.listdir(student_dir_path):

                        submit_dir_path = os.path.join(student_dir_path, submit_dir)
                        # print(submit_dir_path)
                        if os.path.isdir(submit_dir_path):
                            # print("submit time:"+submit_dir)
                            result_whitebox = {}
                            result_blackbox = {}

                            for content in os.listdir(submit_dir_path):
                                if not content.startswith('.') and content.endswith('.c'):
                                    print(content)
                                    #content_path = os.path.join(submit_dir_path, content)
                                    exe_command(submit_dir_path,'clang checksum.c')
                                    #execute whitebox testing
                                    for i in range(1,N_White+1):
                                        # if your Os is Linux, you need to change a.exe -> ./a.out.
                                        command = 'a.exe < '+ whitebox_path+str(i)+".in"
                                        print(command)
                                        try:
                                            test_output = exe_command(submit_dir_path, command)
                                            #The first parameter is status and the second is the output
                                            key = test_output[1] == standardOutouts_whitebox[i-1]

                                        except UnicodeDecodeError:
                                            key = False
                                            print('UnicodeDecodeError')
                                        result_whitebox[i] = int(key)
                                    #execute black box testing
                                    for i in range(1,N_Black+1):
                                        # if your Os is Linux, you need to change a.exe -> ./a.out.
                                        command = 'a.exe < '+ blackbox_path+str(i)+".in"
                                        print(command)
                                        try:
                                            test_output = exe_command(submit_dir_path, command)
                                            #The first parameter is status and the second is the output
                                            key = test_output[1]==standardOutouts_blackbox[i-1]

                                        except UnicodeDecodeError:
                                            key = False
                                            print('UnicodeDecodeError')
                                        result_blackbox[i] = int(key)

                            all_result_white[submit_dir_path]=result_whitebox
                            all_result_black[submit_dir_path]=result_blackbox

                            # file = open(submit_dir_path+'\\test_result_white.txt', 'w')
                            # file.write(json.dumps(result_whitebox));
                            # file.close()
                            #
                            # file = open(submit_dir_path + '\\test_result_black.txt', 'w')
                            # file.write(json.dumps(result_blackbox));
                            # file.close()


    with open('labels_whitebox.json','w')as f:
        f.write(json.dumps(all_result_white))
        f.close()

    with open('labels_blackbox.json','w') as f:
        f.write(json.dumps(all_result_black))
        f.close()


    for code_white in all_result_white:
        print(code_white)

    for code_black in all_result_black:
        print(code_black)




if __name__ == '__main__':
    getAllResult('G:\\UIUC\data\iterate\problems','G:\\UIUC\data\iterate\problems\checksum\\tests\whitebox\\','G:\\UIUC\data\iterate\problems\checksum\\tests\\blackbox\\')







