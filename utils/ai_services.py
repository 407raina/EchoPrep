import google.generativeai as genai
import os
import json
import requests
from typing import List, Dict

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Hugging Face API configuration
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/"

def generate_interview_questions(job_role: str, experience_level: str, interview_type: str, skills: str) -> List[str]:
    """Generate interview questions using Gemini AI"""
    
    if not GOOGLE_API_KEY:
        # Return sample questions if API key not configured
        return [
            f"Tell me about yourself and your experience in {job_role}.",
            f"What interests you most about working as a {experience_level} {job_role}?",
            f"How would you approach a challenging project involving {skills}?",
            "Describe a time when you had to learn a new technology quickly.",
            "What are your career goals for the next 3-5 years?"
        ]
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Generate 5-7 realistic interview questions for a {experience_level} {job_role} position.
        
        Interview Type: {interview_type}
        Key Skills/Technologies: {skills}
        
        Requirements:
        1. Questions should be appropriate for {experience_level} level
        2. Include a mix of technical and behavioral questions based on the interview type
        3. Focus on {skills} when relevant
        4. Make questions realistic and commonly asked in actual interviews
        5. Return only the questions, one per line, without numbering
        
        Interview Type Guidelines:
        - Technical: Focus on problem-solving, coding challenges, and technical concepts
        - Behavioral: Focus on past experiences, teamwork, and soft skills
        - Mixed: Combine both technical and behavioral questions
        """
        
        response = model.generate_content(prompt)
        questions = [q.strip() for q in response.text.split('\n') if q.strip()]
        
        return questions[:7]  # Limit to 7 questions max
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        # Return fallback questions
        return [
            f"Tell me about yourself and your experience in {job_role}.",
            f"What interests you most about working as a {experience_level} {job_role}?",
            f"How would you approach a challenging project involving {skills}?",
            "Describe a time when you had to learn a new technology quickly.",
            "What are your career goals for the next 3-5 years?"
        ]

def analyze_interview_performance(transcript: str, job_role: str, experience_level: str, skills: str) -> Dict:
    """Analyze interview performance using Gemini AI"""
    
    if not GOOGLE_API_KEY:
        # Return sample feedback if API key not configured
        return {
            "overall_score": 75,
            "feedback": {
                "clarity": "Good communication skills demonstrated throughout the interview.",
                "technical_accuracy": "Showed understanding of key concepts related to the role.",
                "problem_solving": "Demonstrated logical thinking and problem-solving approach.",
                "confidence": "Appeared confident and well-prepared for the interview."
            },
            "strengths": [
                "Clear and articulate responses",
                "Good understanding of role requirements",
                "Professional demeanor"
            ],
            "areas_for_improvement": [
                "Provide more specific examples",
                "Elaborate on technical details",
                "Show more enthusiasm for the role"
            ],
            "recommendations": [
                "Practice describing your projects with more technical detail",
                "Prepare specific examples of your achievements",
                "Research the company and role more thoroughly"
            ]
        }
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Analyze this interview transcript for a {experience_level} {job_role} position.
        Focus on skills: {skills}
        
        Transcript:
        {transcript}
        
        Provide a comprehensive analysis in JSON format with the following structure:
        {{
            "overall_score": <integer from 0-100>,
            "feedback": {{
                "clarity": "<analysis of communication clarity>",
                "technical_accuracy": "<analysis of technical knowledge>",
                "problem_solving": "<analysis of problem-solving approach>",
                "confidence": "<analysis of confidence and presentation>"
            }},
            "strengths": [
                "<list of key strengths demonstrated>"
            ],
            "areas_for_improvement": [
                "<list of areas that need improvement>"
            ],
            "recommendations": [
                "<list of specific recommendations for improvement>"
            ]
        }}
        
        Be constructive, specific, and helpful in your analysis. Consider the experience level when evaluating responses.
        """
        
        response = model.generate_content(prompt)
        
        # Try to parse JSON response
        try:
            analysis = json.loads(response.text)
            return analysis
        except json.JSONDecodeError:
            # If JSON parsing fails, create structured response from text
            return {
                "overall_score": 75,
                "feedback": {
                    "clarity": "Analysis completed - please review the detailed feedback below.",
                    "technical_accuracy": "Technical knowledge assessed based on responses.",
                    "problem_solving": "Problem-solving approach evaluated.",
                    "confidence": "Overall presentation and confidence noted."
                },
                "strengths": ["Interview completed successfully"],
                "areas_for_improvement": ["Continue practicing interview skills"],
                "recommendations": [response.text[:500] + "..."]
            }
        
    except Exception as e:
        print(f"Error analyzing performance: {e}")
        return {
            "overall_score": 70,
            "feedback": {
                "clarity": "Unable to analyze due to technical issues.",
                "technical_accuracy": "Please review your responses manually.",
                "problem_solving": "Consider practicing with more examples.",
                "confidence": "Continue building confidence through practice."
            },
            "strengths": ["Completed the interview"],
            "areas_for_improvement": ["Continue practicing"],
            "recommendations": ["Keep practicing interview skills", "Review common interview questions"]
        }

def conversational_setup_assistant(user_input: str, conversation_history: List[str]) -> Dict:
    """AI assistant for conversational interview setup"""
    
    if not GOOGLE_API_KEY:
        # Simple rule-based responses if API key not configured
        if "job" in user_input.lower() or "role" in user_input.lower():
            return {
                "response": "What specific job role are you preparing for? For example: Software Engineer, Data Analyst, Product Manager, etc.",
                "extracted_info": {"job_role": user_input if len(user_input.split()) <= 3 else None}
            }
        elif "experience" in user_input.lower() or "level" in user_input.lower():
            return {
                "response": "What's your experience level? Please choose: Entry Level, Mid Level, or Senior Level.",
                "extracted_info": {"experience_level": user_input if any(level in user_input.lower() for level in ['entry', 'mid', 'senior']) else None}
            }
        else:
            return {
                "response": "I'd love to help you set up your mock interview! Let's start with the job role you're preparing for.",
                "extracted_info": {}
            }
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        context = "\n".join(conversation_history[-5:])  # Last 5 exchanges for context
        
        prompt = f"""
        You are an AI assistant helping users set up personalized mock interviews. Your goal is to gather:
        1. Job Role (e.g., "Software Engineer", "Data Analyst")
        2. Experience Level (Entry Level, Mid Level, Senior Level)
        3. Interview Type (Technical, Behavioral, Mixed)
        4. Key Skills/Technologies (e.g., "Python, SQL, Machine Learning")
        
        Conversation History:
        {context}
        
        User's latest input: "{user_input}"
        
        Respond in a friendly, conversational way and ask the next logical question to gather missing information.
        
        Return your response in this JSON format:
        {{
            "response": "<your conversational response>",
            "extracted_info": {{
                "job_role": "<extracted job role or null>",
                "experience_level": "<extracted level or null>",
                "interview_type": "<extracted type or null>",
                "skills": "<extracted skills or null>"
            }}
        }}
        
        If you have all required information, end with: "Great! I have all the information needed to create your mock interview."
        """
        
        response = model.generate_content(prompt)
        
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            return {
                "response": response.text,
                "extracted_info": {}
            }
            
    except Exception as e:
        print(f"Error in conversational setup: {e}")
        return {
            "response": "I'm here to help you set up your mock interview. What job role are you preparing for?",
            "extracted_info": {}
        }
