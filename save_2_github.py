import subprocess
import os

def run_command(command):
    process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    print(process.stdout)
    if process.stderr:
        print(process.stderr)

def save_to_github(repo_path, commit_message):
    try:
        # Change to the repository directory
        os.chdir(repo_path)
        
        # Add changes to staging
        run_command('git add .')
        
        # Commit changes
        run_command(f'git commit -m "{commit_message}"')
        
        # Push changes to the remote repository
        run_command('git push origin main')  # Adjust the branch name if necessary

        print("Changes have been pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    repo_path = '/path/to/your/repo'  # Update this to your repository path
    commit_message = 'Automated commit message'  # Update this to your desired commit message

    save_to_github(repo_path, commit_message)
