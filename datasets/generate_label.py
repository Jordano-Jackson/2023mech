import os
import json
import re

# image path list 
image_paths = [
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/지6.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6 (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6 (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/지6belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/지6belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/허6belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/지6belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/손6belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7 (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/김7belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8 (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/이8belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/정우5.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/정우5 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/정우5belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/정우5belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/정우5belt (3).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt (4).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt (5).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/수인5belt (6).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/0.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/0 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/1 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/2belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/3belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/4belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/5belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/6belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/7belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/8belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/9belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/10belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/11belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/12belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13 (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13 (2)_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13_1.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13belt.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/13belt (2).jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/14.jpg',
    '/home/csjihwanh/Desktop/Projects/2023mech/datasets/level_data/14 (2).jpg',
]

# data generate
data = []
for i, path in enumerate(image_paths):
    # extract the number from the name of the file 
    # caution : this is not completely works, you SHOULD manually check the generated json file
    level_match = re.search(r'(\d+)(?: \(\d+\))?(?:belt)?\.jpg', os.path.basename(path))
    if level_match:
        level = int(level_match.group(1))
    else:
        level = None
    
    entry = {
        'name': str(i + 1),
        'link': path,
        'level': level
    }
    data.append(entry)


# save data in JSON format
with open('metadata.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print('metadata has been generated.')
