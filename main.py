from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, presence_of_all_elements_located

import sys, getopt

cf_login_url='https://codeforces.com/enter'
at_login_url='https://atcoder.jp/login'
# contest_url='https://codeforces.com/contest/1515'


import os, fnmatch
# https://stackoverflow.com/questions/1724693/find-a-file-in-python
# find('*.txt', '/path/to/dir')
def find(pattern, path='./'):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def read_login_password(login_line_num, password_line_num, login_file_string):
    with open(login_file_string, 'r') as login_data_file:
        lines=login_data_file.readlines()
        username=lines[login_line_num]
        password=lines[password_line_num]
    return username,password

def cf_read_login_password(login_file_string="login_data"):
    return read_login_password(0,1,login_file_string)

def at_read_login_password(login_file_string="login_data"):
    return read_login_password(2,3,login_file_string)


def cf_login(driver,wait,login_text,password_text):
    driver.get(cf_login_url)
    driver.find_element(By.CSS_SELECTOR, "#handleOrEmail").send_keys(login_text)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password_text)
    driver.find_element(By.CSS_SELECTOR, ".submit").click()
    first_result = wait.until(presence_of_element_located((By.XPATH, "//div[@id='pageContent']")))

def at_login(driver,wait,login_text,password_text):
    driver.get(at_login_url)
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(login_text)
    print("log")
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password_text)
    print("pass")
    # driver.find_element(By.XPATH, "//button[@id='submit']").click()
    # print("click")
    first_result = wait.until(presence_of_element_located((By.XPATH, "//div[@class='col-sm-8']")))


def cf_get_problemset(driver,wait,problemset_url):
    driver.get(problemset_url)
    problems = wait.until(presence_of_all_elements_located((By.XPATH, "//table[@class='problems']/tbody/tr/td[1]/a")))
    problems_url=[]
    for p in problems:
        print(p.get_attribute("href"))
        problems_url.append(p.get_attribute("href"))
    return problems_url


    
def cf_get_test_cases(driver,wait,problem_url):
    sections = problem_url.split('/')
    problem_name_upper = sections[-1].upper()
    problem_name_lower = sections[-1].lower()

    driver.get(problem_url)

    outputs = wait.until(presence_of_all_elements_located((By.XPATH, "//div[@class='sample-test']/div[2]/pre")))
    inputs  = wait.until(presence_of_all_elements_located((By.XPATH, "//div[@class='sample-test']/div[1]/pre")))
    assert(len(inputs) == len(outputs))
    input_text=[]
    output_text=[]
    for i in inputs:
        input_text.append(i.get_attribute("textContent"))
    for i in outputs:
        output_text.append(i.get_attribute("textContent"))
    
    test_case = list(zip(input_text, output_text))
    return test_case

# 'A', 'https://codeforces.com/contest/1519'
#   -> 'https://codeforces.com/contest/1519/problem/A'
def cf_problem_name_to_url(name, contest_url):
    return contest_url+'/problem/'+name

# https://codeforces.com/problemset/problem/1519/E link from problemset page
# https://codeforces.com/contest/1519/problem/E    link from contest page
def cf_contest_name_to_url(name):
    if name.startswith('https'):
        return name
    url_prefix='https://codeforces.com/contest/'
    return url_prefix+name

def cf_parse_problem_names(names):
    return names.upper();

def cf_process(contest_url, problems_name, file_path, problem_passing):
    with webdriver.Chrome() as driver:
        login_text,password_text=cf_read_login_password()
        wait = WebDriverWait(driver, 10)

        cf_login(driver,wait,login_text, password_text)
        problems_url=[]
        if problems_name=='':
            problems_url = cf_get_problemset(driver,wait,contest_url)
        else:
            for problem_name in problems_name:
                problems_url.append(cf_problem_name_to_url(problem_name, contest_url))
        print(problems_name)
        
        for problem_url in problems_url:
            sections = problem_url.split('/')
            problem_name_upper = sections[-1].upper()
            problem_name_lower = sections[-1].lower()
            if problem_passing:
                # a*.(in|out)
                pattern_for_infile = problem_name_lower+'*.in'
                # TODO: apply file_path
                if len(find(pattern_for_infile))>0:
                    continue
            
            test_case = cf_get_test_cases(driver,wait,problem_url)
            # writing test to files
            file_name=problem_name_lower
            for test_num in range(len(test_case)):
                test = test_case[test_num]
                i, o = test
                in_suffix='.in'
                out_suffix='.out'
                common_prefix = problem_name_lower+str(test_num+1)
                # eg. f1.in f2.in f3.in
                # TODO: appy file_path
                input_filename=common_prefix+in_suffix
                output_filename=common_prefix+out_suffix
                
                # INPUT FILE
                with open(input_filename, 'w') as in_f:
                    print(i, file=in_f)
                # OUTPUT FILE
                with open(output_filename, 'w') as out_f:
                    print(o, file=out_f)

        


# https://atcoder.jp/contests/abc200/tasks
def at_get_problemset(driver,wait,problemset_url):
    driver.get(problemset_url)
    problems = wait.until(presence_of_all_elements_located((By.XPATH, "//table[@class='table table-bordered table-striped']/tbody/tr/td[1]/a")))
    problems_url=[]
    for p in problems:
        print(p.get_attribute("href"))
        problems_url.append(p.get_attribute("href"))
    return problems_url

# https://atcoder.jp/contests/abc200
# https://atcoder.jp/contests/abc200/tasks
def at_contest_name_to_url(name):
    if name.startswith('https'):
        # TODO: check if it is tasks tab
        return name
    url_prefix='https://atcoder.jp/contests/'
    task_url_suffix='/tasks'
    return url_prefix+name+task_url_suffix

def at_parse_problem_names(names):
    return names.lower();

# 'a', 'https://atcoder.jp/contests/abc200/tasks'
#   -> 'https://atcoder.jp/contests/abc200/tasks/abc200_a'
def at_problem_name_to_url(name, contest_name, contest_url):
    return contest_url+'/'+contest_name+"_"+name

def at_get_problem_name_from_url(problem_url):
    sections = problem_url.split('/')
    problem_name = sections[-1].split('_')[-1]
    return problem_name

def at_get_test_cases(driver,wait,problem_url):
    problem_name_upper = at_get_problem_name_from_url(problem_url).upper()
    problem_name_lower = problem_name_upper.lower()

    driver.get(problem_url)
    xpath_for_test_parts="//div[@id='task-statement']/span/span[@class='lang-en']/div[@class='part']/section/pre[1]"
    parts = wait.until(presence_of_all_elements_located((By.XPATH, xpath_for_test_parts)))
    input_text=[]
    output_text=[]
    # zip it with 0/1 and map
    for i in range(len(parts)):
        part=parts[i]
        text = part.get_attribute("textContent")
        # input
        if i%2==0:
            input_text.append(text)
        else:
            output_text.append(text)
    assert(len(input_text) == len(output_text))
    
    test_case = list(zip(input_text, output_text))
    return test_case

# contest_url, problems_name, file_path, problem_passing
def at_process(contest_tasks_url, contest_name, problems_name, file_path, problem_passing):
    with webdriver.Chrome() as driver:
        login_text,password_text=at_read_login_password()
        wait = WebDriverWait(driver, 10)

        at_login(driver,wait,login_text, password_text)
        print('success')
        problems_url=[]
        if problems_name=='':
            problems_url = at_get_problemset(driver,wait,contest_tasks_url)
        else:
            for problem_name in problems_name:
                problems_url.append(at_problem_name_to_url(problem_name,contest_name, contest_tasks_url))
        print(problems_name)
        
        # https://atcoder.jp/contests/abc200/tasks/abc200_e
        for problem_url in problems_url:
            print(problem_url)
            problem_name = at_get_problem_name_from_url(problem_url)
            print(problem_name)
            problem_name_upper = problem_name.upper()
            problem_name_lower = problem_name_upper.lower()

            if problem_passing:
                # a*.(in|out)
                pattern_for_infile = problem_name_lower+'*.in'
                # TODO: apply file_path
                if len(find(pattern_for_infile))>0:
                    continue
            
            test_case = at_get_test_cases(driver,wait,problem_url)

            # writing test to files
            for test_num in range(len(test_case)):
                test = test_case[test_num]
                i, o = test
                in_suffix='.in'
                out_suffix='.out'
                common_prefix = problem_name_lower+str(test_num+1)
                # eg. f1.in f2.in f3.in
                # TODO: appy file_path
                input_filename=common_prefix+in_suffix
                output_filename=common_prefix+out_suffix
                
                # INPUT FILE
                with open(input_filename, 'w') as in_f:
                    print(i, file=in_f)
                # OUTPUT FILE
                with open(output_filename, 'w') as out_f:
                    print(o, file=out_f)


# TODO: add login password passing as arguments, some file or args
# TODO: add -p 1519/E option
# main.py -c 1519
# download problemset and all test for each problem
# main.py -c 1519 -s aBcdF
# download problems [A, B, C, D, E] from contest 1519
# main.py -c 1519 -s aBcdF -p
# download problems [A, B, C, D, E] from contest 1519
# only if there is no a*.in, a*.out for problem A,
# ..., f*.in, f*.out for problem F 
def main(argv):
    contestst_pass=''
    problem_pass=''
    problem_passing=False
    contest_pass=''
    file_path='./'
    help_string='main.py -c <contest number> [-p] list of selected problems' + '\n    -x makes passing problems with at least one test' + '\n    [-f] path to in out files'
    at_coder_mode=False

    try:
        opts, args = getopt.getopt(argv,"axhc:p:f:",["contest=","problem=","filePath="])
        # print(opts)
        # print(args)
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        # print(opts)
        if opt == '-h':
            print(help_string)
            sys.exit()
        elif opt in ("-c", "--contest"):
            contest_pass = arg
        elif opt in ("-p", "--problem"):
            problem_pass = arg
        elif opt in ("-f", "--file_path"):
            filePath = arg
        elif opt in ("-x"):
            problem_passing=True
        elif opt in ("-a"):
            at_coder_mode=True

    print("contest=\'",end='')
    print(contest_pass+"\'")
    print("problem=\'",end='')
    print(problem_pass+"\'")
    print("file_path=\'",end='')
    print(file_path+"\'")

    if at_coder_mode==False:
        contest_url = cf_contest_name_to_url(contest_pass)
        problems_name_upper = cf_parse_problem_names(problem_pass)

        print("contest_url=\'",end='')
        print(contest_url+"\'")

        print("problems_name_upper=\'",end='')
        print(problems_name_upper+"\'")

        print("passing ...")
        cf_process(contest_url, problems_name_upper, file_path, problem_passing)
    else:
        contest_tasks_url = at_contest_name_to_url(contest_pass)
        problems_name_lower = at_parse_problem_names(problem_pass)

        print("contest_url=\'",end='')
        print(contest_tasks_url+"\'")

        print("problems_name_upper=\'",end='')
        print(problems_name_lower+"\'")

        print("passing ...")
        at_process(contest_tasks_url, contest_pass, problems_name_lower, file_path, problem_passing)



if __name__ == "__main__":
    main(sys.argv[1:])