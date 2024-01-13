import json
from openai import OpenAI
from http.server import BaseHTTPRequestHandler

def cover_letter(input):
  format="info: {name: Olivier Saint-Vincent,email: olivier520100@gmail.com,number: 4385302718,addres: 105 Rue Saint-Judes}, workexperience: {title: Project Manager (ASSUME THE JOB TITLE IF NOT ANNOUNCED),company: Microsoft,period: Jan 1st 2024 - Feb 2nd 2024,description: Led a team of engineers to build a button for azure (JOBS DESCRIPTION ONLY)},skills: [{name: Python,rating: 4},{name: Java,rating: 3}],languages: [{name: English,rating: 4},{name: French,rating: 5}],education: [{institution: College Bois-de-Boulogne,degree: DEC,year: 2024}]}"


  OpenAI.api_key = "PRIVATE_OPENAI_KEY"
  client = OpenAI(api_key="PRIVATE_OPENAI_KEY")

  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },

    messages=[
      {
        "role": "system",
        "content": "You are an assistant that is going to write a professional cover letter from a job application. You will use the users personnal information and qualifications that would be useful concerning the job the user is applying for"
      },
      {
        "role": "user",
        "content":input   
      }
    ],
    

  )
  return json.loads(response.choices[0].message.content)



class handler(BaseHTTPRequestHandler):

   def do_POST(self):
         content_length = int(self.headers['Content-Length'])
         post_data = self.rfile.read(content_length)
         received_data = str(post_data.decode('utf-8'))
         json_data = json.loads(cover_letter(received_data))

         self.send_response(200)
         self.send_header('Content-type', 'application/json')
         self.end_headers()
         self.wfile.write(json_data.encode('utf-8'))
