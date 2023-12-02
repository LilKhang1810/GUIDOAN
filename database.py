path = '/Users/nguyenkhanghuu/Downloads/AI_DB.txt'
def save(line):
    try:
        f=open(path,'a',encoding='utf8')
        f.writelines(line)
        f.writelines('\n')
        f.close()
    except:
        pass
def read():
    taskList = []
    try:
        f = open(path, 'r', encoding='utf8')
        for line in f:
            data = line.strip()
            arr = data.split('-')
            if len(arr) == 3:
                task = {
                    'name': arr[0].strip(),
                    'deadline': int(arr[1].strip()),
                    'satisfy': int(arr[2].strip())
                }
                taskList.append(task)
        f.close()
    except:
        pass
    return taskList


