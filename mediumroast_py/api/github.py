from github import Github
import base64
import json
import time
import requests
from requests.auth import HTTPBasicAuth

__license__ = "Apache 2.0"
__copyright__ = "Copyright (C) 2024 Mediumroast, Inc."
__author__ = "Michael Hay"
__email__ = "hello@mediumroast.io"
__status__ = "Production"

class GitHubFunctions:
    """
    A class used to interact with GitHub's API.

    This class encapsulates the functionality for interacting with GitHub's API,
    including methods for getting user information, repository information, and
    managing lock files.

    Attributes
    ----------
    token : str
        The personal access token for GitHub's API.
    org_name : str
        The name of the organization on GitHub.
    repo_name : str
        The name of the repository on GitHub.
    repo_desc : str
        The description of the repository on GitHub.
    github_instance : Github
        An instance of the Github class from the PyGithub library.
    lock_file_name : str
        The name of the lock file.
    main_branch_name : str
        The name of the main branch in the repository.
    object_files : dict
        A dictionary mapping object types to their corresponding file names.
    """
    def __init__(self, token, org, process_name):
        """
        Constructs all the necessary attributes for the GitHubFunctions object.

        Parameters
        ----------
        token : str
            The personal access token for GitHub's API.
        org : str
            The name of the organization on GitHub.
        process_name : str
            The name of the process using the GitHubFunctions object.
        """
        self.token = token
        self.org_name = org
        self.repo_name = f"{org}_discovery"
        self.repo_desc = "A repository for all of the mediumroast.io application assets."
        self.github_instance = Github(token)
        self.lock_file_name = f"{process_name}.lock"
        self.main_branch_name = 'main'
        self.object_files = {
            'Studies': 'Studies.json',
            'Companies': 'Companies.json',
            'Interactions': 'Interactions.json',
            'Users': None,
            'Billings': None
        }

    def get_sha(self, container_name, file_name, branch_name):
        """
        Get the SHA of a specific file in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container (directory) in the repository.
        file_name : str
            The name of the file for which to get the SHA.
        branch_name : str
            The name of the branch in which the file is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a dictionary with status information, and the SHA of the file (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            contents = repo.get_contents(f"{container_name}/{file_name}", ref=branch_name)
            return [True, {'status_code': 200, 'status_msg': f'captured sha for [{container_name}/{file_name}]'}, contents.sha]
        except Exception as e:
            return [False, {'status_code': 500, 'status_msg': f'unable to capture sha for [{container_name}/{file_name}] due to [{str(e)}]'}, str(e)]

    def get_user(self):
        """
        Get information about the current user.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the user's raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            user = self.github_instance.get_user()
            return [True, 'SUCCESS: able to capture current user info', user.raw_data]
        except Exception as e:
            return [False, f'ERROR: unable to capture current user info due to [{str(e)}]', str(e)]
        
    def get_all_users(self):
        """
        Get all users who are collaborators on the repository.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and a list of users' raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            collaborators = repo.get_collaborators()
            return [True, 'SUCCESS: able to capture info for all users', [collaborator.raw_data for collaborator in collaborators]]
        except Exception as e:
            return [False, f'ERROR: unable to capture info for all users due to [{str(e)}]', str(e)]

    def create_repository(self):
        """
        Create a new repository in the organization.

        The repository name and description are taken from the instance attributes `self.repo_name` and `self.repo_desc`.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, and the newly created repository's raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            org = self.github_instance.get_organization(self.org_name)
            repo = org.create_repo(self.repo_name, description=self.repo_desc, private=True)
            return [True, repo]
        except Exception as e:
            return [False, str(e)]
    
    def get_actions_billings(self):
        """
        Get the actions billings information for the organization.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the actions billings information as a dictionary (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            url = f"https://api.github.com/orgs/{self.org_name}/settings/billing/actions"
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.token))

            if response.status_code == 200:
                return [True, 'SUCCESS: able to capture actions billings info', response.json()]
            else:
                return [False, f'ERROR: unable to capture actions billings info due to [{response.status_code}]', None]
        except Exception as e:
            return [False, f'ERROR: unable to capture actions billings info due to [{str(e)}]', str(e)]

    def get_storage_billings(self):
        """
        Get the storage billings information for the organization.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the storage billings information as a dictionary (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            url = f"https://api.github.com/orgs/{self.org_name}/settings/billing/shared-storage"
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.token))

            if response.status_code == 200:
                return [True, 'SUCCESS: able to capture storage billings info', response.json()]
            else:
                return [False, f'ERROR: unable to capture storage billings info due to [{response.status_code}]', None]
        except Exception as e:
            return [False, f'ERROR: unable to capture storage billings info due to [{str(e)}]', str(e)]
    
    def get_github_org(self):
        """
        Get the organization's information.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, and the organization's raw data (or the error message in case of failure).
        """
        try:
            org = self.github_instance.get_organization(self.org_name)
            return [True, org.raw_data]
        except Exception as e:
            return [False, str(e)]
        
    def create_branch_from_main(self):
        """
        Create a new branch from the main branch.

        Parameters
        ----------
        branch_name : str
            The name of the new branch to be created.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the new branch's raw data (or the error message in case of failure).
        """
        branch_name = str(int(time.time()))
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            main_branch = repo.get_branch(self.main_branch_name)
            ref = repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)
            return [True, f"SUCCESS: created branch [{branch_name}]", ref.raw_data]
        except Exception as e:
            return [False, f"FAILED: unable to create branch [{branch_name}] due to [{str(e)}]", None]

    def merge_branch_to_main(self, branch_name, commit_description='Performed CRUD operation on objects.'):
        """
        Merge a branch into the main branch.

        Parameters
        ----------
        branch_name : str
            The name of the branch to be merged.
        commit_description : str, optional
            The description of the commit, by default 'Performed CRUD operation on objects.'

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the pull request's raw data (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            pull = repo.create_pull(title=commit_description, body=commit_description, head=branch_name, base=self.main_branch_name)
            if pull.mergeable:
                pull.merge(commit_message=commit_description)
                return [True, 'SUCCESS: Pull request created and merged successfully', pull.raw_data]
            else:
                return [False, 'FAILED: Pull request not created or merged successfully due to merge conflict', None]
        except Exception as e:
            return [False, f"FAILED: Pull request not created or merged successfully due to [{str(e)}]", None]
        
    def check_for_lock(self, container_name):
        """
        Check if a container is locked.

        Parameters
        ----------
        container_name : str
            The name of the container to check.

        Returns
        -------
        list
            A list containing a boolean indicating whether the container is locked or not, a status message, and the lock status (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            contents = repo.get_contents(container_name)
            lock_exists = any(content.path == f"{container_name}/{self.lock_file_name}" for content in contents)
            if lock_exists:
                return [True, f"container [{container_name}] is locked with lock file [{self.lock_file_name}]", lock_exists]
            else:
                return [False, f"container [{container_name}] is not locked with lock file [{self.lock_file_name}]", lock_exists]
        except Exception as e:
            return [False, str(e), None]

    def lock_container(self, container_name):
        """
        Lock a container by creating a lock file in it.

        Parameters
        ----------
        container_name : str
            The name of the container to lock.
        branch_name : str
            The name of the branch where the container is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the lock file's raw data (or the error message in case of failure).
        """
        lock_file = f"{container_name}/{self.lock_file_name}"
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            latest_commit = repo.get_commits()[0]
            lock_response = repo.create_file(lock_file, f"Locking container [{container_name}]", "", branch=self.main_branch_name)
            return [True, f"SUCCESS: Locked the container [{container_name}]", lock_response.raw_data]
        except Exception as e:
            return [False, f"FAILED: Unable to lock the container [{container_name}]", str(e)]

    def unlock_container(self, container_name, commit_sha, branch_name=None):
        """
        Unlock a container by deleting the lock file in it.

        Parameters
        ----------
        container_name : str
            The name of the container to unlock.
        branch_name : str
            The name of the branch where the container is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the lock file's raw data (or the error message in case of failure).
        """
        lock_file = f"{container_name}/{self.lock_file_name}"
        branch_name = branch_name if branch_name else self.main_branch_name
        lock_exists = self.check_for_lock(container_name)
        if lock_exists[0]:
            try:
                repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
                file_contents = repo.get_contents(lock_file, ref=branch_name)
                unlock_response = repo.delete_file(lock_file, f"Unlocking container [{container_name}]", file_contents.sha, branch=branch_name)
                return [True, f"SUCCESS: Unlocked the container [{container_name}]", unlock_response.raw_data]
            except Exception as e:
                return [False, f"FAILED: Unable to unlock the container [{container_name}]", str(e)]
        else:
            return [False, f"FAILED: Unable to unlock the container [{container_name}]", None]
        
    def delete_blob(self, container_name, file_name, branch_name, sha):
        """
        Delete a blob (file) in a container (directory) in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container where the blob is located.
        file_name : str
            The name of the blob to delete.
        branch_name : str
            The name of the branch where the blob is located.
        sha : str
            The SHA of the blob to delete.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the delete response's raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            file_path = f"{container_name}/{file_name}"
            file_contents = repo.get_contents(file_path, ref=branch_name)
            delete_response = repo.delete_file(file_path, f"Delete object [{file_name}]", file_contents.sha, branch=branch_name)
            return [True, { 'status_code': 200, 'status_msg': f'deleted object [{file_name}] from container [{container_name}]' }, delete_response.raw_data]
        except Exception as e:
            return [False, { 'status_code': 503, 'status_msg': f'unable to delete object [{file_name}] from container [{container_name}]' }, str(e)]

    def write_blob(self, container_name, file_name, blob, branch_name, sha=None):
        """
        Write a blob (file) to a container (directory) in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container where the blob will be written.
        file_name : str
            The name of the blob to write.
        blob : str
            The content to write to the blob.
        branch_name : str
            The name of the branch where the blob will be written.
        sha : str, optional
            The SHA of the blob to update. If None, a new blob will be created.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the write response's raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            file_path = f"{container_name}/{file_name}"
            blob = base64.b64encode(blob.encode()).decode()
            if sha:
                file_contents = repo.get_contents(file_path, ref=branch_name)
                write_response = repo.update_file(file_path, f"Update object [{file_name}]", blob, file_contents.sha, branch=branch_name)
            else:
                write_response = repo.create_file(file_path, f"Create object [{file_name}]", blob, branch=branch_name)
            return [True, f"SUCCESS: wrote object [{file_name}] to container [{container_name}]", write_response.raw_data]
        except Exception as e:
            return [False, f"ERROR: unable to write object [{file_name}] to container [{container_name}]", str(e)]

    def write_object(self, container_name, obj, ref, my_sha):
        """
        Write an object to a container in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container where the object will be written.
        obj : dict
            The object to write.
        branch_name : str
            The name of the branch where the object will be written.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the write response's raw data (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            file_path = f"{container_name}/{self.object_files[container_name]}"
            content = base64.b64encode(json.dumps(obj).encode()).decode()
            file_contents = repo.get_contents(file_path, ref=ref)
            write_response = repo.update_file(file_path, f"Update object [{self.object_files[container_name]}]", content, file_contents.sha, branch=ref)
            return [True, f"SUCCESS: wrote object [{self.object_files[container_name]}] to container [{container_name}]", write_response.raw_data]
        except Exception as e:
            return [False, f"ERROR: unable to write object [{self.object_files[container_name]}] to container [{container_name}]", str(e)]
        
    def read_objects(self, container_name, branch_name=None):
        """
        Read all objects from a container in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container from which to read objects.
        branch_name : str
            The name of the branch where the container is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the objects' raw data (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            branch_name = branch_name if branch_name else self.main_branch_name
            file_path = f"{container_name}/{self.object_files[container_name]}"
            file_contents = repo.get_contents(file_path, ref=branch_name)
            decoded_content = base64.b64decode(file_contents.content).decode()
            return [True, f"SUCCESS: read objects from container [{container_name}]", json.loads(decoded_content)]
        except Exception as e:
            return [False, f"ERROR: unable to read objects from container [{container_name}]", str(e)]
    
    def update_object(self, container_name, obj, ref, my_sha):
        """
        Update an object in a container in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container where the object is located.
        obj : dict
            The object to update.
        branch_name : str
            The name of the branch where the object is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the update response's raw data (or the error message in case of failure).
        """
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            file_path = f"{container_name}/{self.object_files[container_name]}"
            content = base64.b64encode(json.dumps(obj).encode()).decode()
            file_contents = repo.get_contents(file_path, ref=ref)
            write_response = repo.update_file(file_path, f"Update object [{self.object_files[container_name]}]", content, file_contents.sha, branch=ref)
            return [True, f"SUCCESS: updated object [{self.object_files[container_name]}] in container [{container_name}]", write_response.raw_data]
        except Exception as e:
            return [False, f"ERROR: unable to update object [{self.object_files[container_name]}] in container [{container_name}]", str(e)]

    def delete_object(self, container_name, file_name, branch_name, sha):
        """
        Delete an object from a container in a specific branch.

        Parameters
        ----------
        container_name : str
            The name of the container from which to delete the object.
        obj : dict
            The object to delete.
        branch_name : str
            The name of the branch where the object is located.

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, a status message, and the delete response's raw data (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        try:
            repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
            file_path = f"{container_name}/{file_name}"
            file_contents = repo.get_contents(file_path, ref=branch_name)
            delete_response = repo.delete_file(file_path, f"Delete object [{file_name}]", file_contents.sha, branch=branch_name)
            return [True, { 'status_code': 200, 'status_msg': f'deleted object [{file_name}] from container [{container_name}]' }, delete_response.raw_data]
        except Exception as e:
            return [False, { 'status_code': 503, 'status_msg': f'unable to delete object [{file_name}] from container [{container_name}]' }, str(e)]
        
    def create_containers(self, containers=['Studies', 'Companies', 'Interactions']):
        """
        Create multiple containers (directories) in the repository.

        Parameters
        ----------
        containers : list, optional
            The names of the containers to create, by default ['Studies', 'Companies', 'Interactions'].

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, and a list of responses for each container creation (or the error message in case of failure).
        """
        return [False, f'initial port completed but implementation unconfirmed, untested and unsupported', None]
        responses = []
        empty_json = base64.b64encode(json.dumps([]).encode()).decode()
        for container_name in containers:
            try:
                repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
                file_path = f"{container_name}/{container_name}.json"
                response = repo.create_file(file_path, f"Create container [{container_name}]", empty_json)
                responses.append(response)
            except Exception as e:
                responses.append(str(e))
        return [all(isinstance(res, Github.GitCommit.GitCommit) for res in responses), responses]
    
    def catch_container(self, containers=['Studies', 'Companies', 'Interactions']):
        """
        Catch (lock) multiple containers (directories) in the repository.

        Parameters
        ----------
        containers : list, optional
            The names of the containers to catch, by default ['Studies', 'Companies', 'Interactions'].

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, and a list of responses for each container catch (or the error message in case of failure).
        """
        responses = []
        for container_name in containers:
            try:
                repo = self.github_instance.get_repo(f"{self.org_name}/{self.repo_name}")
                file_path = f"{container_name}/{container_name}.json"
                file_contents = repo.get_contents(file_path)
                decoded_content = base64.b64decode(file_contents.content).decode()
                responses.append([True, json.loads(decoded_content)])
            except Exception as e:
                responses.append([False, str(e)])
        return responses
    
    def release_container(self, repo_metadata):
        """
        Release (unlock) multiple containers (directories) in the repository.

        Parameters
        ----------
        containers : list, optional
            The names of the containers to release, by default ['Studies', 'Companies', 'Interactions'].

        Returns
        -------
        list
            A list containing a boolean indicating success or failure, and a list of responses for each container release (or the error message in case of failure).
        """
        for container in repo_metadata['containers']:
            # Unlock branch
            branch_unlocked = self.unlock_container(container, repo_metadata['containers'][container]['lockSha'], repo_metadata['branch']['name'])
            if not branch_unlocked[0]:
                return [False, {'status_code': 503, 'status_msg': f"Unable to unlock the container, objects may have been written please check [{container}] for objects and the lock file."}, branch_unlocked]
            # Unlock main
            main_unlocked = self.unlock_container(container, repo_metadata['containers'][container]['lockSha'])
            if not main_unlocked[0]:
                return [False, {'status_code': 503, 'status_msg': f"Unable to unlock the container, objects may have been written please check [{container}] for objects and the lock file."}, main_unlocked]
        # Return success with number of objects written
        return [True, {'status_code': 200, 'status_msg': f"Released [{len(repo_metadata['containers'])}] containers."}, None]
    
