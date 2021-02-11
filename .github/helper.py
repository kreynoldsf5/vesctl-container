import requests
import json
import os

try:
    GHworkspace = os.environ.get("GITHUB_WORKSPACE")
except Exception as e:
    print(e)
GLurl = "https://gitlab.com/api/graphql"
GLquery = "{}/.github/GLquery.json".format(GHworkspace)
DHurl = "https://hub.docker.com/v2/repositories/kreynoldsf5/vesctl/tags"
DLpath = "{}/vesctl.linux-amd64.gz".format(GHworkspace)


def VesctlInfo(s):
    try:
        with open(GLquery) as f:
            data = json.load(f)
        resp = s.post(GLurl, json=data)
        resp.raise_for_status()
        stuff = json.loads(resp.text)
        tag = stuff[0]['data']['project']['releases']['nodes'][0]['tagName']
        linkList = stuff[0]['data']['project']['releases']['nodes'][0]['assets']['links']['nodes']
        link = next(item for item in linkList if item["name"] == "vesctl.linux-amd64.gz")['directAssetUrl']
    except Exception as e:
        print(e)
    return {
        'tag': tag,
        'link': link
    }
    
def HubTagExist(s, tag):
    try:
        resp = s.get(DHurl)
        resp.raise_for_status()
        results = json.loads(resp.text)['results']
        tagExists = next((item for item in results if item["name"] == tag), None)
    except Exception as e:
        print(e)
    if tagExists:
        return True
    return False

def DLrelease(s, DLurl):
    try:
        resp = s.get(DLurl)
        resp.raise_for_status()
        with open(DLpath, 'wb') as f:
            f.write(resp.content)
    except Exception as e:
        print(e)

def main():
    s = requests.Session()
    GHenv = os.environ.get("GITHUB")
    vesInfo = VesctlInfo(s)
    hubTagExist = HubTagExist(s, vesInfo['tag'])
    if hubTagExist:
        os.system('echo "build_container=false" >> $GITHUB_ENV')
        print("Docker Hub container is up to date")
    else:
        print("Update to Docker Hub container needed")
        DLrelease(s, vesInfo['link'])
        print("Downloaded latest vesctl release")
        os.system('echo "build_container=true" >> $GITHUB_ENV')
        os.system('echo "tag={}" >> $GITHUB_ENV'.format(vesInfo['tag']))
        print("Set build env vars")

if __name__ == "__main__":
    main()