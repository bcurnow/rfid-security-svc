#!/usr/bin/env python3
"""
Standalone script to regenerate the API key for rfidsecuritysvc.
"""
import sys
from pathlib import Path
import click

# Add the parent directory to the path so we can import rfidsecuritysvc
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rfidsecuritysvc.db.dbms import init_db
from rfidsecuritysvc.util.auth import generate_api_key


def main():
    """Main entry point for the genkey binary."""
    if not click.confirm('Are you sure? This will invalidate the current API key.'):
        click.echo('Aborted.')
        sys.exit(0)
    
    try:
        # Initialize database (creates connection, schema, etc.)
        init_db()
        
        # Generate new API key
        key = generate_api_key()
        click.echo(click.style(f'Generated new API key: "{key}"', fg='green'))
        click.echo(click.style('Please record this value as it will not be printed again.', fg='yellow'))
    
    except Exception as e:
        click.echo(click.style(f'Error: {e}', fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
