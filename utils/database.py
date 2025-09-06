import sqlite3
import hashlib
import uuid
from datetime import datetime
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/interviews.db")

def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Interview mocks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interview_mocks (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        job_role TEXT NOT NULL,
        experience_level TEXT NOT NULL,
        interview_type TEXT NOT NULL,
        skills TEXT NOT NULL,
        questions TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Interview sessions table (for storing conversation transcripts)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interview_sessions (
        id TEXT PRIMARY KEY,
        interview_mock_id TEXT NOT NULL,
        transcript TEXT,
        feedback TEXT,
        score INTEGER,
        completed_at TIMESTAMP,
        FOREIGN KEY (interview_mock_id) REFERENCES interview_mocks (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        user_id = str(uuid.uuid4())
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
            (user_id, username, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(username, password):
    """Verify user credentials and return user_id if valid"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    return result['id'] if result else None

def create_interview_mock(user_id, job_role, experience_level, interview_type, skills):
    """Create a new interview mock"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    mock_id = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO interview_mocks (id, user_id, job_role, experience_level, interview_type, skills)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (mock_id, user_id, job_role, experience_level, interview_type, skills))
    
    conn.commit()
    conn.close()
    
    return mock_id

def get_user_interviews(user_id):
    """Get all interview mocks for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, job_role, experience_level, interview_type, skills, completed, 
           datetime(created_at, 'localtime') as created_at
    FROM interview_mocks 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    ''', (user_id,))
    
    interviews = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return interviews

def get_interview_mock(mock_id):
    """Get specific interview mock details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM interview_mocks WHERE id = ?
    ''', (mock_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

def update_interview_questions(mock_id, questions):
    """Update interview questions for a mock"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE interview_mocks SET questions = ? WHERE id = ?
    ''', (questions, mock_id))
    
    conn.commit()
    conn.close()

def create_interview_session(mock_id, transcript, feedback, score):
    """Create interview session record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    session_id = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO interview_sessions (id, interview_mock_id, transcript, feedback, score, completed_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, mock_id, transcript, feedback, score, datetime.now()))
    
    # Mark interview mock as completed
    cursor.execute('''
    UPDATE interview_mocks SET completed = TRUE WHERE id = ?
    ''', (mock_id,))
    
    conn.commit()
    conn.close()
    
    return session_id

def get_interview_session(mock_id):
    """Get interview session for a mock"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM interview_sessions WHERE interview_mock_id = ?
    ''', (mock_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

def get_user_stats(user_id):
    """Get user statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed
    FROM interview_mocks 
    WHERE user_id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    
    total = result['total'] if result else 0
    completed = result['completed'] if result else 0
    success_rate = (completed / total * 100) if total > 0 else 0
    
    conn.close()
    
    return {
        'total': total,
        'completed': completed,
        'success_rate': success_rate
    }
