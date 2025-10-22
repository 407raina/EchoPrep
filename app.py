from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

# Delegate to existing main application
import main as echomain

echomain.main()
