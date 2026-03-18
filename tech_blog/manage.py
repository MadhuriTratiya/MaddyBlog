import os
import sys
import dotenv

def main():
    # 1. Load environment variables
    dotenv.load_dotenv()

    # 2. Set Django Settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tech_blog.settings')
    
    # NOTE: We removed oracledb.init_oracle_client() to use "Thin Mode".
    # This is recommended for Oracle Autonomous Database connections.

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()