import requests
import json
import multiprocessing

SPACE_ID = "CHANGE_ME"
COOKIES = {"token_v2": "CHANGE_ME"}
PROCESSES = 8

def get_page_id_list():
    json_data = {
        "type": "BlocksInSpace",
        "query": "",
        "filters": {
            "isDeletedOnly": True,
            "excludeTemplates": False,
            "navigableBlockContentOnly": True,
            "requireEditPermissions": False,
            "includePublicPagesWithoutExplicitAccess": False,
            "ancestors": [],
            "createdBy": [],
            "editedBy": [],
            "lastEditedTime": {},
            "createdTime": {},
            "inTeams": [],
        },
        "sort": {
            "field": "lastEdited",
            "direction": "desc",
        },
        "limit": 1000,
        "spaceId": SPACE_ID,
        "source": "trash",
    }

    response = requests.post("https://www.notion.so/api/v3/search", cookies=COOKIES, json=json_data)
    parsed_results = json.loads(response.text)["results"]

    return [p["id"] for p in parsed_results]

def delete_page_by_id(id):
    json_data = {
        "blocks": [
            {
                "id": id,
                "spaceId": SPACE_ID,
            },
        ],
        "permanentlyDelete": True,
    }

    response = requests.post("https://www.notion.so/api/v3/deleteBlocks", cookies=COOKIES, json=json_data)
    print("Deleting page:", id)
    print("Status code:", response.status_code, "\n")


if __name__ == "__main__":
    pool = multiprocessing.Pool(PROCESSES)
    
    stop = False
    while(not stop):
        id_list = get_page_id_list()
        if len(id_list) == 0:
            stop = True

        pool.map(delete_page_by_id, id_list)

    print("Trash is empty!")