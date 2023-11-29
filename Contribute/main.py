import os
import json
import shutil

# Load the json
f = open('form.json')
form = json.load(f)
f.close()

data = {
    "Cross-site Leak (XSLeak)": "xsleak.md",
    "Cross-site Scripting (XSS)": "xss.md",
    "Command Injection": "command-injection.md",
    "Open redirect": "open-redirect.md",
    "Local File Inclusion (LFI)": "lfi.md",
    "GraphQL batch": "graphql-batch.md",
    "Template Injection":"template-injection.md",
    "Cache Poisoning": "cache-poisoning.md"
}

# CTF has to be single value
def check_single_value(form, field):
    return type(form[field]) == str and bool(form[field].strip())

# For every chall must be a description, at least 1 category, at least 1 author, solves number, at least 1 writeup and filename
def check_consistency(form):
    fields = ["Challenges", "Descriptions", "Category", "Authors", "Solves", "Writeups", "Filename"]
    return all(type(form.get(field, [])) == list for field in fields)

def move_files(form):
    chall_sources = []
    chall_directory = form["CTF"].split("@")[0].lower().replace(" ", "")

    for i in form["Challenges"]:
        chall_sources.append("../files/" + chall_directory + "/" + i.lower().replace(" ", "-"))
        os.makedirs("../files/" + chall_directory + "/" + i.lower().replace(" ", "-"))
    
    for i in form["Filename"]:
        shutil.move("files/"+i, chall_sources[0] + "/" + i.lower().replace(" ", "-"))
        chall_sources.pop(0)

# Returns the output path
def create_ctf(form):
    substitutions = {
        "Ctf": form["CTF"].split("@")[0],
        "Ctf_ctftime": form["CTF"].split("@")[1],
        "Team": form["Team"].split("@")[0],
        "Team_ctftime": form["Team"].split("@")[1],
        "Weight": form["Weight"]
    }

    chall_directory = form["CTF"].split("@")[0].lower().replace(" ", "")
    output_directory = os.path.join("../gitbook/challenges", chall_directory)
    output_path = os.path.join(output_directory, "README.md")

    os.makedirs(output_directory, exist_ok=True)

    with open("gitbook-template/ctf-template.md", 'r', encoding='utf-8') as template_file, open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(template_file.read().format(**substitutions))

    with open("../gitbook/challenges/README.md", "r") as file:
        lines = file.readlines()

    lines.insert(3, "* [{}]({}/README.md)".format(form["CTF"].split("@")[0], chall_directory)+"\n")

    with open("../gitbook/challenges/README.md", "w") as file:
        file.writelines(lines)

    with open("../gitbook/SUMMARY.md", "r") as file:
        lines = file.readlines()

    lines.insert(4, "  * [{}](challenges/{}/README.md)".format(form["CTF"].split("@")[0], chall_directory)+"\n")

    with open("../gitbook/SUMMARY.md", "w") as file:
        file.writelines(lines)

    return output_directory

def add_challs(form, output_directory):
    template = "| [{}](/gitbook/challenges/"+form["CTF"].split("@")[0].lower().replace(" ", "")+"/{}.md) |  [{}](/gitbook/categories/{})   | {}  | [@{}]({})"
    for i in range(len(form["Challenges"])):
        for index, key in enumerate(data.keys(), start=1):
            if form["Category"][i] == str(index):
                category = key
                category_path = data[key]
        with open("../gitbook/categories/"+category_path, 'a', encoding='utf-8') as file:
            file.write("* [{} ({})]({}/{}.md)\n".format(form["Challenges"][i], form["CTF"].split("@")[0],output_directory[2:],form["Challenges"][i].lower().replace(" ", "-")))
        with open(output_directory+"/README.md", 'a', encoding='utf-8') as file:
            file.write(template.format(form["Challenges"][i], form["Challenges"][i].lower().replace(" ", "-"), category, category_path, form["Solves"][i], form["Authors"][i].split("@")[0], form["Authors"][i].split("@")[1]) + '\n')

def create_chall_posts(form, output_directory):
    for i in range(len(form["Challenges"])):
        substitutions = {
            "Ctf": form["CTF"].split("@")[0].lower().replace(" ", ""),
            "Challenge": form["Challenges"][i],
            "Challenge_Path": form["Challenges"][i].lower().replace(" ", "-"),
            "Description": form["Descriptions"][i],
            "Writeup": form["Writeups"][i].split("@")[0],
            "Writeup_url": form["Writeups"][i].split("@")[1]
        }
        with open("gitbook-template/challenge-template.md", 'r', encoding='utf-8') as template_file, open(output_directory+"/"+form["Challenges"][i].lower().replace(" ", "-")+".md", 'w', encoding='utf-8') as output_file:
            output_file.write(template_file.read().format(**substitutions))


move_files(form)
out = create_ctf(form)
add_challs(form, out)
create_chall_posts(form, out)