import os
import subprocess
import requests
import json
import base64


def update_text():
    maven_path = r"C:\apache-maven-4.0.0-alpha-5-bin\apache-maven-4.0.0-alpha-5\bin\mvn.cmd"
    #->idk
    maven_project_dir = r"C:\Users\-----\-----\GetInfo"
    #->"https://github.com/carter4299/custom-PPO-Notebook/tree/main/market_cap_updater/GetInfo"
    subprocess.run([maven_path, "clean", "install", "-f", maven_project_dir], check=True)
    subprocess.run([maven_path, "exec:java", "-Dexec.mainClass=org.example.Main", "-f", maven_project_dir], check=True)



def update_csv(df):
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')
    repo = 'custom-PPO-Notebook'
    file_path = 'data/tick_info.csv'

    url_get = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}'
    headers = {'Authorization': 'token {}'.format(token)}
    response_get = requests.get(url_get, headers=headers)
    if response_get.status_code == 200:
        sha = response_get.json()['sha']
    else:
        print('Could not obtain SHA for the file. Error: ', response_get.json())
        return

    csv_content = df.to_csv(index=False)
    csv_content_encoded = base64.b64encode(csv_content.encode()).decode()

    data = {
        "message": "update csv file",
        "committer": {
            "name": username,
            "email": "-----------@gmail.com"
        },
        "content": csv_content_encoded,
        "sha": sha
    }

    url_put = f'https://api.github.com/repos/{username}/{repo}/contents/{file_path}'
    response_put = requests.put(url_put, headers=headers, data=json.dumps(data))

    return response_put.json()


