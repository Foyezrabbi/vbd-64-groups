import json
from facebook import GraphAPI, GraphAPIError

class FacebookPoster:
    def __init__(self, access_token):
        """
        Initialize the FacebookPoster class with the user's access token.
        
        :param access_token: Facebook user access token for authentication
        """
        self.graph = GraphAPI(access_token)

    def post_to_group(self, group_id, message):
        """
        Post a message to a specific group.
        
        :param group_id: The ID of the Facebook group
        :param message: The message to post
        """
        try:
            response = self.graph.put_object(parent_object=group_id, connection_name='feed', message=message)
            print(f"Successfully posted to group {group_id}. Post ID: {response['id']}")
        except GraphAPIError as e:
            print(f"Failed to post to group {group_id}. Error: {e}")

    def post_to_multiple_groups(self, group_data_file):
        """
        Post a message to multiple groups based on a JSON configuration file.
        
        :param group_data_file: Path to the JSON file containing group details and message
        """
        try:
            with open(group_data_file, 'r') as file:
                data = json.load(file)
            
            groups = data.get("groups", [])
            message = data.get("message", "")
            
            if not groups or not message:
                raise ValueError("JSON file must contain 'groups' (list) and 'message' (string).")
            
            for group_id in groups:
                self.post_to_group(group_id, message)
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            print(f"Error reading or processing the JSON file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    # Replace with your Facebook user access token
    ACCESS_TOKEN = "your_access_token_here"
    
    # Example JSON file content
    # {
    #     "groups": ["group_id_1", "group_id_2", "group_id_3"],
    #     "message": "Hello, this is a test message from my Python script!"
    # }
    GROUP_DATA_FILE = "group_data.json"  # Path to your JSON file

    facebook_poster = FacebookPoster(ACCESS_TOKEN)
    facebook_poster.post_to_multiple_groups(GROUP_DATA_FILE)
