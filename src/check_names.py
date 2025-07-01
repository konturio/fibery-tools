from log import get_logger
log = get_logger(__name__)

import csv

with open('tasknames.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['id', 'name', 'url', 'status'])
    for task in reader:
        issues = []
        name = task['name']
        url = task['url']
        ciname = ' ' + name.lower().strip() + ' '
        if task['status'] not in ('Canceled', 'Done'):
            if ' support for ' in ciname:
                issues.append("Remove 'support for'")
            if ' ability ' in ciname:
                issues.append("Remove 'ability'")
            if ' add ' in ciname:
                issues.append("Remove 'add'")
            if ciname.startswith(' make '):
                issues.append("Remove 'make'")
            if ciname.startswith(' do '):
                issues.append("Remove 'do'")
            if ciname.startswith(' implement '):
                issues.append("Remove 'implement'")
            if ciname.startswith(' develop '):
                issues.append("Remove 'develop'")
            if ciname.startswith(' create '):
                issues.append("Remove 'create'")
            if ciname.startswith(' we '):
                issues.append("Remove 'we' and reword")
            if ciname.startswith(' there is '):
                issues.append("Remove 'there is' and reword")
            if ciname.startswith(' rework '):
                issues.append("Remove 'rework' and mention target result instead")
            if ciname.startswith(' try '):
                issues.append("Do. Or do not. There is no try. (Master Yoda)")
            if ciname.startswith(' think '):
                issues.append("Replace 'think' with actual expected artifact")
            if ' feature ' in ciname:
                issues.append("Remove 'feature'")
            if ' improve ' in ciname:
                issues.append("Remove 'improve'")
            if ' the ' in ciname:
                issues.append("It is ok to lose 'the' in headlines")
#            if ' panel with ' in ciname or ' panels with ' in ciname:
#                issues.append("'Panel with X' can become 'X Panel' in headlines")

            if ' with ' in ciname:
                issues.append("'A with B' can often become 'B A' in headlines")
            if ' for ' in ciname:
                issues.append("'A for B' can often become 'B A' in headlines")
                
            if 'ing ' in ciname and not 'warning' in ciname and not 'hosting' in ciname and not 'missing' in ciname and not 'meeting' in ciname and not 'staging' in ciname and not 'onboarding' in ciname and not 'logging' in ciname and not 'monitoring' in ciname:
                issues.append("Gerund in name, 'ing' found. Reword as target state, not process.")
                
            # branding
            if ' disaster.ninja' in ciname or 'disaster ninja' in ciname:            
                issues.append("Shorten 'Disaster Ninja' to DN or DN2")
            if ' Hot' in name:
                issues.append("'HOT' is spelled in all-caps")
            if 'dn2' in ciname and not 'DN2' in name:
                issues.append("'DN2' is spelled in all-caps")
            if 'emdat' in ciname:
                issues.append("'DN2' is spelled in all-caps with dash")
            if ' pdc' in ciname and not 'PDC' in name:
                issues.append("'PDC' is spelled in all-caps")
            if ' poi ' in ciname and not ' POI' in name:
                issues.append("'POI' is spelled in all-caps")
            if ' api' in ciname and not ' API' in name:
                issues.append("'API' is spelled in all-caps")
                
            if ' sp ' in ciname:
                issues.append("'SP' can mean Story Point, Stored Procedure or Summer Party, rename")

            if ' k2' in ciname:
                issues.append("'K2' is deprecated, use Platform instead")
            if ' events api' in ciname:
                issues.append("'Event API' is spelled in singular")
            
            if ' - ' in ciname:
                issues.append("Name contains ' - '. Simplify.")
            if ', ' in ciname:
                issues.append("Name contains ', '.  Summarize or break out in several items.")
            if '. ' in ciname:
                issues.append("Name contains '. '.  Simplify.")
            if ('User_Story' in url and len(name) > 35):
                issues.append('Name is longer than 35 characters, UI will show "%s"'%name[:35])
            if (len(name) > 60) and not 'User_Story' in url:
                issues.append('Name is longer than 60 characters, UI will show "%s"'%name[:60])

                
            if issues:# and 'User_Story' in url:
                log.info(f"{task['url']} {name}")
                for issue in issues:
                    log.info(' - %s.' % issue.strip('.'))
                log.info("")
                #print(len(issues), name, task['url'], issues)
