from http.server import BaseHTTPRequestHandler
import json
from openai import OpenAI


format="info: {name: Olivier Saint-Vincent, email: olivier520100@gmail.com,number: 4385302718,addres: 105 Rue Saint-Judes}, workexperience: {title: Project Manager (ASSUME THE JOB TITLE IF NOT ANNOUNCED),company: Microsoft,period: Jan 1st 2024 - Feb 2nd 2024,description: Led a team of engineers to build a button for azure (JOBS DESCRIPTION ONLY)},skills: [{name: Python},{name: Java}],languages: [{name: English},{name: French}],education: [{institution: College Bois-de-Boulogne,degree: DEC,year: 2024}]}"

def gpt(input):
    OpenAI.api_key = "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"
    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    response_format={ "type": "json_object" },

    messages=[
        {
        "role": "system",
        "content": "You will be provided with unstructured data, and your task is to parse it into json format like this "+format+"DO NOT DEVIATE FROM THE EXACT NAMES OF THE SUBTITLES, EVEN IF THE INFORMATION IN THE PARAGRAPH IS NOT IN THE SAME ORDER AS THE FORMAT I SHOWED U YOU NEED TO FOLLOW TO FORMAT, also if something is unspecified dont forget to just write unspecified instead of not putting the subtitle. DONT FORGET THAT THIS IS FOR A CV SO IT NEEDS TO BE PROFESSIONAL AT A MINIMUM."
        },
        {
        "role": "user",
        "content":input   
        }
    ],
    )
    
    return json.loads(response.choices[0].message.content)













def json_to_html(data):
    # HTML Initialize
    html_initial = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Curriculum Vitae</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }}

        h1, h2 {{
            color: #333;
        }}

        h2 {{
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}

        ul {{
            list-style-type: none;
            padding: 0;
        }}

        li {{
            margin-bottom: 5px;
        }}
    </style>
</head>
<body>
'''.format(name=data['info']['name'])

    # HTML Contact Info
    html_info = '''
    <header>
        <h1>{name}</h1>
    </header>

    <section>
        <h2>Contact Information</h2>
        <ul>
            <li>Email: {email}</li>
            <li>Phone: {number}</li>
            <li>Address: {address}</li>
        </ul>
    </section>
    '''.format(**data['info'])

    # HTML Education Info
    html_education = '''
    <section>
        <h2>Education</h2>
        {education_content}
    </section>
    '''.format(education_content='\n'.join(
        '<p>{}, {}, {}</p>'.format(edu['institution'], edu['degree'], edu['year']) for edu in data['education']
    ))

    # HTML Work Experience
    html_job = '''
    <section>
        <h2>Work Experience</h2>
        {job_content}
    </section>
    '''.format(job_content='\n'.join(
        '<p>{} - {} - {}</p><ul><li>{}</li></ul>'.format(job['company'], job['title'], job['period'], job['description'])
        for job in data['workexperience']
    ))

    # HTML Skills
    html_skills = '''
    <section>
        <h2>Skills</h2>
        <ul>
            {skills_content}
        </ul>
    </section>
    '''.format(skills_content='\n'.join('<li>{}</li>'.format(skill['name']) for skill in data['skills']))

    # HTML Languages
    html_languages = '''
    <section>
        <h2>Languages</h2>
        <ul>
            {languages_content}
        </ul>
    </section>
    '''.format(languages_content='\n'.join('<li>{}</li>'.format(language['name']) for language in data['languages']))

    html_end = '''
</body>
</html>
'''

    return (html_initial + html_info + html_education + html_job + html_skills + html_languages + html_end)



        

received_data = "I am am olivier saint-vincent. age 19, 105 Rue saint judes, olivier520100@gmail.com. Worked at pianoheritage as a saleman a did web development in 2018-2021. Worked at crux climbing gym from 2022-2023. Good at c, python pytorch, machine learning. Speak french and english and russian and tagalog"
fagg_t = (gpt(received_data))
print(fagg_t)