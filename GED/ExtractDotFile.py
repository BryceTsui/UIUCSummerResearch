import os


def extractCFile(root):

    c_files = [];
    for problem in os.listdir(root):

        problem_path = os.path.join(root, problem)

        if os.path.isdir(problem_path):
            #print("problem"+problem)
            for student_dir in os.listdir(problem_path):
                #print(student_dir)

                student_dir_path = os.path.join(problem_path,student_dir)
                if os.path.isdir(student_dir_path):
                    #print("student:"+student_dir)

                    for submit_dir in os.listdir(student_dir_path):

                        submit_dir_path = os.path.join(student_dir_path,submit_dir)
                        #print(submit_dir_path)
                        if os.path.isdir(submit_dir_path):
                            #print("submit time:"+submit_dir)

                            for content in os.listdir(submit_dir_path):
                                if not content.startswith('.') and content.endswith('.c'):
                                    #print(content)
                                    content_path = os.path.join(submit_dir_path,content)
                                    c_files.append(content_path)

    return c_files


def extractDotFile(root):

    dot_files = [];
    for problem in os.listdir(root):

        problem_path = os.path.join(root, problem)

        if os.path.isdir(problem_path):
            #print("problem"+problem)
            for student_dir in os.listdir(problem_path):
                #print(student_dir)

                student_dir_path = os.path.join(problem_path,student_dir)
                if os.path.isdir(student_dir_path):
                    #print("student:"+student_dir)

                    for submit_dir in os.listdir(student_dir_path):

                        submit_dir_path = os.path.join(student_dir_path,submit_dir)
                        #print(submit_dir_path)
                        if os.path.isdir(submit_dir_path):
                            #print("submit time:"+submit_dir)

                            for content in os.listdir(submit_dir_path):
                                if not content.startswith('.') and content.endswith('.dot'):
                                    #print(content)
                                    content_path = os.path.join(submit_dir_path,content)
                                    dot_files.append(content_path)

    return dot_files

def exe_command(work_path,command):

    #save the original dir then we can change to the original dir after executing command
    original_cwd = os.getcwd()
    print(original_cwd)
    os.chdir(work_path)
    os.system(command)

    os.chdir(original_cwd)






if __name__ =='__main__':
    problems_path = 'G:\\UIUC\iterate\problems'

    #You need to change the path to the problems path
    c_files = extractCFile(problems_path)
    print(len(c_files))

    for file_path in c_files:
        command = 'clang '+ file_path +' -c -emit-llvm'# compile file without optimizing

        #I have executed this line and generated the .bc file
        #exe_command(os.path.dirname(file_path), command)

        #execute command looks like this: ./llvm-dg-dump  ~/UIUC/iterate-data/checksum-1.bc > ~/UIUC/iterate-data/checksum-1.dot
        command = './llvm-dg-dump '+file_path.replace('.c','.bc') +" > "+ file_path.replace('.c','.dot')
        #exe_command('/home/xgy/UIUC/dg/build/tools',command)

    dot_file = extractDotFile(problems_path)
    print(dot_file)


