import subprocess
import sys
import os
import subprocess
import threading
import socket
import re

class RunCCode(object):
    def __init__(self, code=None,index=0):
        self.code = code
        self.index =  index
        self.compiler = "gcc"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_c_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_c_prog(self, cmd="./running/a.out",idx=0):
        #taking custom input
        my_input = open("./running/input"+str(idx)+".txt","r")

        memory_limit = 5024 #default value, TODO: fetch from the DB
        time_limit = 2 #default TODO fetch from the DB
        virtualenvcmd = "./timeout -m "+str(memory_limit)
        cmd = cmd+" "+str(time_limit)
        p = subprocess.Popen(virtualenvcmd+" "+cmd,stdin=my_input,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        #checking if memory exceeded
        arr = self.stderr.split()
        if(arr[0]=="MEM"):
            #if the memory limit exceeded
            ERROR = "MEMORY LIMIT EXCEEDED \n"
            self.stdout = self.stdout + ERROR
        elif(arr[0]=="FINISHED"):
            MSG = "Running successful\n"
            self.stdout = self.stdout + MSG

    

    def run_c_code(self, code=None):
        def cleanup_files(index):
            prog_output = "./running/a"+str(self.index)+".out"
            filename = "./running/test"+str(self.index)+".c"
            inputfile = "./running/input"+str(self.index)+".txt"
            os.remove(prog_output)
            os.remove(filename)
            os.remove(inputfile)
        idx = self.index
        prog_output = "./running/a"+str(idx)+".out"
        filename = "./running/test"+str(idx)+".c"
        if not code:
            code = self.code
        result_run = "No run done"
        line_to_add = '#include "../setlimits.c"\n'
        code = line_to_add + code
        code =re.sub(r'main[\s \t \n a-z A-Z ( ) , \* ;\[\]]*{', "main(int argc,char* argv[]){ setlimits(argc,argv);", code)
        
        print(code)
        with open(filename, "w") as f:
            f.write(code)
        
        #self.line_prepender(filename,line_to_add)
        res = self._compile_c_code(filename,prog_output)
        print("COMPILED")
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_c_prog(prog_output,idx)
            result_run = self.stdout + self.stderr
        cleanup_files(idx)
        return result_compilation, result_run


    #include the limits file in the users code    
    def line_prepender(self,filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line + content)

    def line_pre_adder(self,filename, line_to_prepend):
        f = fileinput.input(filename, inplace=1)
        for xline in f:
            if f.isfirstline():
                print(line_to_prepend.rstrip('\r\n') + '\n' + xline)
            else:
                print(xline)

    def add_limits(code):
        code = re.sub(r'main[\s \t \n a-z A-Z ( ) , \* ;\[\]]*', "main(int argc,char* argv[]){ setlimits(argc,argv);", code)
        return code





class RunCppCode(object):

    def __init__(self, code=None):
        self.code = code
        self.compiler = "g++"
        if not os.path.exists('running'):
            os.mkdir('running')

    def _compile_cpp_code(self, filename, prog="./running/a.out"):
        cmd = [self.compiler, filename, "-Wall", "-o", prog]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def _run_cpp_prog(self, cmd="./running/a.out"):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_cpp_code(self, code=None):
        filename = "./running/test.cpp"
        if not code:
            code = self.code
        result_run = "No run done"
        with open(filename, "w") as f:
            f.write(code)
        res = self._compile_cpp_code(filename)
        result_compilation = self.stdout + self.stderr
        if res == 0:
            self._run_cpp_prog()
            result_run = self.stdout + self.stderr
        return result_compilation, result_run

class RunPyCode(object):
    
    def __init__(self, code=None):
        self.code = code
        if not os.path.exists('running'):
            os.mkdir('running')

    def _run_py_prog(self, cmd="a.py"):
        cmd = [sys.executable, cmd]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result
    
    def run_py_code(self, code=None):
        filename = "./running/a.py"
        if not code:
            code = self.code
        with open(filename, "w") as f:
            f.write(code)
        self._run_py_prog(filename)
        return self.stderr, self.stdout
