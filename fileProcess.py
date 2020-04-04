import os

#去除小说中的广告

path = r'G:\PythonProject\paChong\books\推理'

new_path = r'G:\PythonProject\paChong\temp'
for a, b, c in os.walk(path):
    print(c)
for i in c:
    f = os.path.join(path, i)
    nf = os.path.join(new_path, i)
    if f.endswith("txt"):
        print(f)
        with open(f, 'r') as oldFile:
            for line in oldFile.readlines():
                content = line.strip()
                if content not in '支付宝搜索“276997”，领取支付宝红包，最高99元，每天可领取1次！':
                    with open(nf, 'a') as newFile:
                        newFile.write(content + '\n')




