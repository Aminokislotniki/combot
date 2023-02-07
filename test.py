new_user_id = 210944655
group_id = -1001847105342

import json
with open('groups/' + str(group_id) + '.json', 'r', encoding='utf-8') as f:
    list_group = json.loads(f.read())
    buf = []
    for x in range(len(list_group['subscribers_del'])):
        if list_group['subscribers_del'][x]['id_user'] == new_user_id:
            del list_group['subscribers_del'][x]



    #     buf.append(x['id_user'])
    # if new_user_id in buf:
    #     del list_group['subscribers_del'][x]
    print(buf)



    # with open("groups/" + str(group_id) + ".json", "w", encoding="utf-8") as f:
    #     json.dump(list_group, f, ensure_ascii=False, indent=4)