import sqlite3
import hashlib
import os
import json
from datetime import datetime

def get_db_path():
    """Get the database file path"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'echoprep.db')

def init_database():
    """Initialize the EchoPrep database with required tables"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create interviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_role TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                interview_type TEXT NOT NULL,
                skills TEXT,
                questions TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create responses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                ai_feedback TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        ''')

        # Create interview_sessions table (stores transcript and feedback)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interview_id INTEGER NOT NULL,
                transcript TEXT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (interview_id) REFERENCES interviews (id)
            )
        ''')

        # Ensure questions column exists for older databases
        cursor.execute("PRAGMA table_info(interviews)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'questions' not in columns:
            try:
                cursor.execute("ALTER TABLE interviews ADD COLUMN questions TEXT")
            except Exception:
                pass
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        raise

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """Verify user credentials"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {'id': user[0], 'username': user[1]}
        return None
        
    except Exception as e:
        print(f"❌ User verification error: {e}")
        return None

def create_user(username, email, password):
    """Create a new user account"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "Account created successfully"
        
    except sqlite3.IntegrityError:
        return False, "Username or email already exists"
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return False, f"Error creating account: {e}"

def get_user_interviews(user_id):
    """Get all interviews for a specific user"""
    db_path = get_db_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM interviews WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        
        interviews = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        interview_list = []
        for interview in interviews:
            interview_list.append({
                'id': interview[0],
                'user_id': interview[1],
                'job_role': interview[2],
                'experience_level': interview[3],
                'interview_type': interview[4],
                'skills': interview[5],
                'questions': interview[6],
                'completed': interview[7],
                'created_at': interview[8]
            })
        
        return interview_list
        
    except Exception as e:
        print(f"❌ Error fetching interviews: {e}")
        return []


# --- Interview creation and retrieval ---

def create_interview_mock(user_id: int, job_role: str, experience_level: str, interview_type: str, skills: str) -> int:
    """Create an interview record and pre-generate questions."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO interviews (user_id, job_role, experience_level, interview_type, skills, completed)
            VALUES (?, ?, ?, ?, ?, FALSE)
            """,
            (user_id, job_role, experience_level, interview_type, skills)
        )
        interview_id = cursor.lastrowid

        # Generate questions using AI service (fallbacks built-in)
        try:
            from utils.ai_services import generate_interview_questions
            normalized_level = experience_level
            # Normalize common labels
            for prefix in ["Entry", "Mid", "Senior", "Lead"]:
                if experience_level.lower().startswith(prefix.lower()):
                    normalized_level = prefix + " Level"
                    break
            questions = generate_interview_questions(job_role, normalized_level, interview_type, skills)
            update_interview_questions(interview_id, questions)
        except Exception as e:
            print(f"⚠️ Failed to generate questions: {e}")

        conn.commit()
        return interview_id
    finally:
        conn.close()


def update_interview_questions(interview_id: int, questions_list) -> None:
    """Store generated questions JSON on interview."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE interviews SET questions = ? WHERE id = ?",
            (json.dumps(list(questions_list or [])), interview_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_interview_mock(interview_id: int):
    """Fetch interview by id with parsed questions."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM interviews WHERE id = ?", (interview_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0],
            'user_id': row[1],
            'job_role': row[2],
            'experience_level': row[3],
            'interview_type': row[4],
            'skills': row[5],
            'questions': row[6],
            'completed': row[7],
            'created_at': row[8],
        }
    finally:
        conn.close()


# --- Interview sessions and completion ---

def create_interview_session(interview_id: int) -> int:
    """Create a new interview session stub and return its id."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO interview_sessions (interview_id, transcript, feedback) VALUES (?, ?, ?)",
            (interview_id, None, None)
        )
        session_id = cursor.lastrowid
        conn.commit()
        return session_id
    finally:
        conn.close()


def get_interview_session(interview_id: int):
    """Get the latest session for an interview, if any."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, interview_id, transcript, feedback, created_at FROM interview_sessions WHERE interview_id = ? ORDER BY created_at DESC LIMIT 1",
            (interview_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0],
            'interview_id': row[1],
            'transcript': row[2],
            'feedback': row[3],
            'created_at': row[4],
        }
    finally:
        conn.close()


def complete_interview_with_responses(interview_id: int, responses) -> None:
    """Mark interview complete, store transcript and AI feedback.

    responses: list of dicts with keys 'question' and 'response'
    """
    # Build transcript text
    transcript_lines = []
    for item in responses or []:
        q = item.get('question', '').strip()
        a = item.get('response', '').strip()
        if q or a:
            transcript_lines.append(f"Q: {q}\nA: {a}")
    transcript = "\n\n".join(transcript_lines)

    # Fetch interview details for context
    interview = get_interview_mock(interview_id)
    job_role = interview.get('job_role', '') if interview else ''
    experience_level = interview.get('experience_level', '') if interview else ''
    skills = interview.get('skills', '') if interview else ''

    # Analyze performance via AI (with fallbacks inside)
    try:
        from utils.ai_services import analyze_interview_performance
        feedback = analyze_interview_performance(transcript, job_role, experience_level, skills)
    except Exception as e:
        print(f"⚠️ Failed to analyze interview: {e}")
        feedback = {
            "overall_score": 75,
            "strengths": ["Completed interview"],
            "improvements": ["Provide more details"],
            "recommendations": ["Keep practicing"]
        }

    # Persist session and mark completed
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO interview_sessions (interview_id, transcript, feedback) VALUES (?, ?, ?)",
            (interview_id, transcript, json.dumps(feedback))
        )
        cursor.execute("UPDATE interviews SET completed = TRUE WHERE id = ?", (interview_id,))
        conn.commit()
    finally:
        conn.close()
