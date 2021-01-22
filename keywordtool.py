import sys
import re
import string
import random
import os
from keywordsearch import Run
# print("{os.getcwd()}\\browser`s drivers\\chromedriver.exe)


files = re.findall(r"\S+.txt", " ".join(sys.argv))
list_of_keywords = []
service = "amazon"

if "--service" in sys.argv:
    service = sys.argv[sys.argv.index("--service") + 1]


print(service)
for file in files:
    with open(file, 'r') as file:
        for line in file:
            list_of_keywords.append(line.split('\n')[0])
print(list_of_keywords)
usernames = ["".join([random.choice(string.ascii_letters) for i in range(20)]) for i in range(len(list_of_keywords))]

if __name__ == "__main__":
    for i in range(len(usernames)):
        Run(usernames[i], list_of_keywords[i], service)
