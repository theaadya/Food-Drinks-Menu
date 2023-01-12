# No KEY required for any of the API
import requests
from pprint import pprint
from prettytable import PrettyTable
import json
from bs4 import BeautifulSoup
while True:
    print('''--------------------------------------MENU--------------------------------------
What are you in the mood for?
1. Eating
2. Drinking
3. Nothing! Get me out of here!''')
    code = int(input('Enter your choice: '))
    if code == 1:
        url = "https://forkify-api.herokuapp.com/api/search"
        resp = requests.get("http://forkify-api.herokuapp.com/phrases.html")
        lst = BeautifulSoup(resp.text, features="html.parser")
        for i in lst(["script", "style"]):
            i.decompose()
        l = list(lst.stripped_strings)
        li = []
        head = ["Ingredients"]
        t = PrettyTable()
        for i in range(2, len(l), 15):
            li.append(l[i:i+15])
        for i in range(len(li)):
            if len(li[i]) == 15:
                t.add_column(head[0], li[i])
            else:
                while len(li[i]) != 15:
                    li[i].append("-")
                t.add_column(head[0], li[i])
        print("\nTo get decided on your meal, have a look at these ingredients.\n")
        print(t)
        user = input("Please enter any one choice of ingredient:\n ")
        query = {'q': user}     
        response = requests.get(url, params=query)
        if response.status_code == 200:
            data = response.json()
            s = len(data['recipes'])
            for i in range(s):
                print(f'{i+1}. {data["recipes"][i]["title"]}')
            dish = int(input("\nPlease select an option number: "))
            answer = data['recipes'][dish-1]['recipe_id']
            url2 = 'https://forkify-api.herokuapp.com/api/get'
            query2 = {'rId': answer}
            resp = requests.get(url2, params=query2)
            if resp.status_code == 200:
                data2 = resp.json()
                print(f'\nYou selected {data["recipes"][dish-1]["title"]}!\n')
                print("Ingredients required are:")
                for i in data2['recipe']['ingredients']:
                    pprint(i.strip())
                print("\nBon Appétit!")
            else:
                print('ERROR')
        else:
            print(f'{response.status_code} Error')
    elif code == 2:
        ans = input("\nTo get decided on your drink of the day please select any one option.\n"
                    "1. I have a drink in mind.\n"
                    "2. No idea! Just give me a random suggestion.\n"
                    "Option: ")
        if ans == "1":
            query = input("\nPlease enter any kind of drink that you would like: ")
            resp = requests.get(
                "http://www.thecocktaildb.com/api/json/v1/1/search.php?",
                params={"s": query
                        }
            )
            d = json.loads(resp.text)
            s = len(d["drinks"])
            for i in range(s):
                pprint(f'{i+1}. {d["drinks"][i]["strDrink"]}')
            n = int(input("\nPlease select an option number: "))
            count = 1
            while count < s+1:
                li, lm = [], []     
                if n == count:
                    res = {k: v for k, v in d["drinks"][count-1].items() if v is not None}
                    for i in range(1, 10):
                        li.append(res.get(f'strIngredient{i}'))
                        lm.append(res.get(f'strMeasure{i}'))
                    while None in li:
                        li.remove(None)
                    while None in lm:
                        lm.remove(None)
                    head = ["Ingredients", "Measure"]
                    t = PrettyTable()
                    if len(li) > len(lm):       
                        while len(li) > len(lm):
                            lm.append("1")
                    elif len(lm) < len(li):
                        while len(li) < len(lm):
                            li.append("1")
                    t.add_column(head[0], li, "l")
                    t.add_column(head[1], lm, "l")
                    print(f'\nYou selected {res["strDrink"]}!\n')
                    print(t)
                    print("\nHere's the method:")
                    ans = res.get("strInstructions").split(".")
                    for i in ans:
                        print(i.strip())
                    print("Cheers!")
                count += 1
        elif ans == "2":
            resp = requests.get("http://www.thecocktaildb.com/api/json/v1/1/random.php")
            d = json.loads(resp.text)
            li, lm = [], []
            res = {k: v for k, v in d["drinks"][0].items() if v is not None}
            for i in range(1, 10):
                li.append(res.get(f'strIngredient{i}'))
                lm.append(res.get(f'strMeasure{i}'))
            while None in li:
                li.remove(None)
            while None in lm:
                lm.remove(None)
            head = ["Ingredients", "Measure"]
            t = PrettyTable()
            if len(li) > len(lm):
                while len(li) > len(lm):
                    lm.append("1")
            elif len(lm) < len(li):
                while len(li) < len(lm):
                    li.append("1")
            t.add_column(head[0], li, "l")
            t.add_column(head[1], lm, "l")
            print(f'\nYou selected {res["strDrink"]}!\n')
            print(t)
            print("\nHere's the method:")
            ans = res.get("strInstructions").split(".")
            for i in ans:
                print(i.strip())
            print("\nCheers!")
    elif code == 3:
        print("\nExiting Application...", "DONE!")
        break
