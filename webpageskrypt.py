import webbrowser
import requests

url = input("Enter the website URL: ")
wayback_api_url = "http://archive.org/wayback/available?url=" + url
response = requests.get(wayback_api_url)
if response.status_code == 200:
    data = response.json()
archived_snapshots = [data['archived_snapshots']['closest']]

for i in range(2):
    timestamp = archived_snapshots[i]['timestamp']
    snapshot_url = f"http://archive.org/wayback/available?url={url}&timestamp={timestamp}"
    response = requests.get(snapshot_url)
    snapshot_data = response.json()
    archived_snapshots.append(snapshot_data['archived_snapshots']['closest'])
    i = 1
    for snapshot in archived_snapshots:
        archived_url = snapshot['url']
        timestamp = snapshot['timestamp']
        file = f"{timestamp}{i}.html"
        i = i + 1

        response = requests.get(archived_url)
        content = response.content

        with open(file, "wb") as f:
            f.write(content)

        print("html saved", file)

        webbrowser.open("file://" + file)
    else:
        print("Couldn't access archive versions")