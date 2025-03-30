from dotenv import load_dotenv
import os
import requests
import json
from psycopg2.extras import Json
from datetime import datetime
import uuid
from typing import Dict, List, Optional,Union
from pydantic import BaseModel, validator
from openai import OpenAI

load_dotenv()
api_key = os.getenv('api_key')

OPENAI_CONFIG = {
    "api_key": api_key,
    "model": "gpt-4o",  # Latest GPT-4o Turbo
    "temperature": 0.3
}
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)

class DamageComponent:
    def __init__(self, name: str, condition: str, repair_action: str, confidence: float = 0.8):
        self.name = name
        self.condition = condition
        self.repair_action = repair_action
        self.confidence = confidence
    
    def to_json(self) -> Dict:
        return {
            "name": self.name,
            "condition": self.condition,
            "repair_action": self.repair_action,
            "confidence": self.confidence
        }
    def to_dict(self):
        return {
            "name": self.name,
            "condition": self.condition,
            "repair_action": self.repair_action,
            "confidence": self.confidence
        }
  
class DamageAssessment:
    def __init__(self, 
                 damage_types: List[str],
                 severity: str,
                 components: List[Union[DamageComponent, Dict]],
                 cost_estimate: Dict[str, float],
                 safety_risk: bool,
                 confidence: float):
        self.damage_types = damage_types
        self.severity = severity
        self.components = components
        self.cost_estimate = cost_estimate
        self.safety_risk = safety_risk
        self.confidence = confidence
    
    def to_json(self) -> Dict:
        return {
            "damage_types": self.damage_types,
            "severity": self.severity,
            "components":json.dumps( self.components),
            "cost_estimate": self.cost_estimate,
            "safety_risk": self.safety_risk,
            "confidence": self.confidence
        }
    def to_dict(self):
        return {
            "damage_types": self.damage_types,
            "severity": self.severity,
            "components": json.dumps(self.components),
            "cost_estimate": self.cost_estimate,
            "safety_risk": self.safety_risk,
            "confidence": self.confidence
        }
    
    # def to_json_string(self) -> str:
    #     return json.dumps(self.to_json(), indent=2)

class DamageAnalyzer:
    def __init__(self):
        self.system_prompt = """
        You are an advanced damage assessment AI. Analyze the following damage report and return:
        - damage_types: Array of damage categories (mechanical/electrical/cosmetic/structural)
        - severity: L1 (minor) to L5 (total loss)
        - components: Array with name, condition, repair_action
        - cost_estimate: parts and labor costs
        - safety_risk: boolean
        - confidence: 0-1 confidence score
        
        Return valid JSON only, with no commentary.
        """
    
    def analyze_damage(self, input_data: dict) -> DamageAssessment:
        """Process damage report through GPT-4"""
        user_prompt = f"""
        Vehicle Data: {input_data.get('vehicle_info', {})}
        Damage Description: {input_data.get('description', '')}
        Visual Evidence: {input_data.get('images', [])}
        Diagnostic Codes: {input_data.get('diagnostics', [])}
        """
        
        response = client.chat.completions.create(
            model=OPENAI_CONFIG["model"],
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=OPENAI_CONFIG["temperature"],
            response_format={"type": "json_object"}
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return DamageAssessment(**result)
        except Exception as e:
            raise ValueError(f"Failed to parse OpenAI response: {str(e)}")

    # def to_dict(self):
    #     """Convert object attributes to a dictionary for JSON serialization"""
    #     return {
    #         "system_prompt": self.system_prompt
    #     }

    # def to_json(self):
    #     """Convert object to JSON"""
    #     return json.dumps(self.to_dict(), indent=4)


url = 'http://localhost:5000/api/'

#insert user to database
# url_register = url +'user/register'
# headers = {"Content-Type": "application/json; charset=utf-8"}
# payload= {"username":"kumar1" ,"email": "kumar1@example.com", "password": "123457"}
# response = requests.post(url_register, headers=headers,json = payload)

# if response.status_code == 201:
#     print('user created successfully')
# else:
#     print('user creation failed')
#     exit()

# login to api
url_login = url +'user/login'
headers = {"Content-Type": "application/json; charset=utf-8"}
payload= {"email": "john@example.com", "password": "123456"}


response = requests.post(url_login, headers=headers,json = payload)
if response.status_code == 200 :
    dict_data = json.loads(response.text)
    token = dict_data.get('token')
    print(token)
else:
    print("error")
    exit()

#get damage data
url_damage = url + 'damage/damagedata'

# Example incoming damage data from the Data Merger
damage_data = {
    "damage_id": "12345",
    "damage_type": "scratches",
    "damage_description": "Visible scratches on the left rear door",
    "severity": "minor",
    "damage_location": "left rear door",
    "images": ["url_to_image1", "url_to_image2"],
    "sensor_data": {
        "impact_force": 250,
        "speed": 15
    },
    "timestamp": "2025-03-22T14:30:00"
}

# Insert data into the knowledge base

headers = {"Content-Type": "application/json; charset=utf-8",'Authorization': 'Bearer' f" {token}"}
response = requests.get(url_damage,headers=headers,json=damage_data)
for x in response.json():
    print(x.get('damage_type'))

assessment_id = str(uuid.uuid4())

url_saveAssessment = url + 'damage/saveAssessment'
sample_data = {
        "vehicle_info": {
            "make": "Toyota",
            "model": "Camry",
            "year": 2020,
            "mileage": 45000
        },
        "description": "Front-end collision at 25mph, visible damage to bumper, hood, and headlights. Airbags deployed.",
        "images": ["front_damage.jpg", "side_view.jpg"],
        "diagnostics": ["B0100", "B1650"]
    }

analyzer = DamageAnalyzer()
assessment = analyzer.analyze_damage(sample_data)
assessment_data = json.dumps(assessment.to_dict()) #assessment.to_json() if hasattr(assessment, 'to_json') else assessment
    
headers = {"Content-Type": "application/json; charset=utf-8",'Authorization': 'Bearer' f" {token}"}
payload = { 'raw_data':sample_data,'assessment':assessment_data,"assessment_id":assessment_id,"model":OPENAI_CONFIG["model"]}

#response = requests.post(url_saveAssessment,headers=headers,json=payload)

data = assessment.to_dict()

url_saveComponent = url + 'damage/saveComponent'

headers = {"Content-Type": "application/json; charset=utf-8",'Authorization': 'Bearer' f" {token}"}
payload = {'components':data['components'],'assessment_id':assessment_id}
response = requests.post(url_saveComponent,headers=headers,json=payload)


def estimate_repair_cost(damage_type, severity):
    cost_estimates = {
        "Scratches": {"Minor": 150, "Major": 300},
        "Dent": {"Minor": 500, "Major": 800},
        "Crack": {"Minor": 400, "Major": 1000},
    }
    
    # Return a default cost if damage type is unknown
    return cost_estimates.get(damage_type, {}).get(severity, 200)

def process_damage_with_gpt(damage_description):
    """
    Uses GPT-4 to process the damage description and generate insights.
    """
    
    # Prepare the prompt for GPT-4 to process damage information
    prompt = f"""
    You are an expert in vehicle damage estimation. Given the following damage description, 
    classify the damage type, severity, and provide an estimated repair cost based on 
    the severity and damage type."""
    
    #Damage description: "{damage_description}"

# Call GPT-4 API to process the damage description
response = client.chat.completions.create(
        engine="gpt-4",  # Specify GPT-4 engine
        prompt=prompt,
        max_tokens=150,  # Limit the output size
        temperature=0.5  # Control randomness; lower is more deterministic
    )

# Extract the response from GPT-4
gpt_output = response.choices[0].text.strip()
    
    # Parse the output to return as structured data
damage_analysis = parse_gpt_output(gpt_output)
    
    # Calculate estimated cost based on the damage type and severity
damage_type = damage_analysis["damage_type"]
severity = damage_analysis["severity"]
estimated_cost = estimate_repair_cost(damage_type, severity)
    
    # Add the estimated repair cost to the result
damage_analysis["estimated_repair_cost"] = f"${estimated_cost}"
    
print( damage_analysis)

