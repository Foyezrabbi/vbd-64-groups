import os
import json
from facebook import GraphAPI, GraphAPIError

class FacebookPoster:
    def __init__(self, access_token):
        """
        Initialize the FacebookPoster class with the user's access token.
        
        :param access_token: Facebook user access token for authentication
        """
        self.graph = GraphAPI(access_token)

    def post_to_group(self, group_id, message, link, image_urls=None):
        """
        Post a message with a URL preview and up to 5 images to a specific group.
        
        :param group_id: The ID of the Facebook group
        :param message: The message to post
        :param link: The URL to share (for preview)
        :param image_urls: List of up to 5 image URLs
        """
        try:
            post_data = {
                "message": message,
                "link": link
            }
            
            if image_urls and len(image_urls) > 0:
                # Facebook allows only one "main" image in the post object.
                post_data["picture"] = image_urls[0]

            response = self.graph.put_object(parent_object=group_id, connection_name='feed', **post_data)
            print(f"Successfully posted to group {group_id}. Post ID: {response['id']}")
        except GraphAPIError as e:
            print(f"Failed to post to group {group_id}. Error: {e}")

    def get_images_from_folder(self, folder_path):
        """
        Retrieve up to 5 image file paths from the specified folder.
        
        :param folder_path: Path to the folder containing images
        :return: List of up to 5 image file paths
        """
        if not os.path.isdir(folder_path):
            print("Invalid folder path.")
            return []

        images = []
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                images.append(os.path.join(folder_path, file_name))
                if len(images) == 5:  # Limit to 5 images
                    break

        if len(images) == 0:
            print("No images found in the folder.")
        
        return images

    def post_to_multiple_groups(self, group_ids, message, link, folder_path=None):
        """
        Post a message with a URL preview and optional images to multiple groups.
        
        :param group_ids: List of Facebook group IDs
        :param message: The message to post
        :param link: The URL to share (for preview)
        :param folder_path: Path to the folder containing images (optional)
        """
        try:
            # Get image URLs from folder
            image_urls = self.get_images_from_folder(folder_path) if folder_path else []

            for group_id in group_ids:
                self.post_to_group(group_id, message, link, image_urls)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    # Replace with your Facebook user access token
    ACCESS_TOKEN = "your_access_token_here"

    # Input JSON file containing group IDs
    GROUP_JSON_FILE = input("Enter the path to the JSON file containing group IDs: ").strip()

    try:
        with open(GROUP_JSON_FILE, 'r') as file:
            data = json.load(file)
            group_ids = data.get("groups", [])
            if not group_ids:
                raise ValueError("No group IDs found in the JSON file.")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Error reading or processing the JSON file: {e}")
        exit()

    # Input message and preview link
    message = input("Enter the message to post: ").strip()
    preview_link = input("Enter the preview link (URL): ").strip()

    # Ask for folder path
    folder_path = input("Enter the path to the folder containing images (leave blank to skip): ").strip()
    folder_path = folder_path if folder_path else None

    # Initialize the FacebookPoster class
    facebook_poster = FacebookPoster(ACCESS_TOKEN)
    facebook_poster.post_to_multiple_groups(group_ids, message, preview_link, folder_path)
