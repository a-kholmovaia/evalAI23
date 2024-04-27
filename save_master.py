
import os

class SaveMaster:

    def __init__(self, directory: str ="saves"):

        # The path to the directory containing the .txt file with the saved flags
        self.directory = directory


    def save_checkpoint(self, scene_id: int) -> None:
        """
        Save the current state of the game (so far only the ID of a current scene)

        Parameters:
        scene_id: int - the scene's ID number
        Returns:
        Void
        """
        # Ensure the directory exists
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Define the path for the new file
        file_path = os.path.join(self.directory, "checkpoint.txt")

        # Open the file and write the current scene's ID
        with open(file_path, 'w') as file:
            file.write(f"Scene ID: {scene_id}\n")

    def load_checkpoint(self) -> int:
        """
        Load the last state of the game (so far only the ID of the last scene)

        Parameters:
        ---
        Returns
        the last played scene's ID if the checkpoint isn't empty, otherwise 0
        """

        # Construct the file path
        file_path = os.path.join(self.directory, f"checkpoint.txt")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Checkpoint file not found.")

        value = 0

        # Read the data from the file
        with open(file_path, 'r') as file:
            try:
                line = file.readlines().pop()
                _, value = line.strip().split(": ")
            except IndexError:
                print("Checkpoint file empty")

        return int(value)


    def save_scene_flags(self, scene_id: int, flags: dict[str, bool]) -> None:
        """
        Save flags of some scene and its scene id

        Parameters:
        scene_id: int - the scene's ID number
        flags: dict[str, bool] - the scene's flags representing completed question sessions
        Returns: 
        Void
        """

        # Ensure the directory exists
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        # Define the path for the new file
        file_path = os.path.join(self.directory, f"scene_{scene_id}.txt")

        # Open the file and write the scene flags
        with open(file_path, 'w') as file:
            # Write scene ID
            file.write(f"Scene ID: {scene_id}\n")
            # Write flags
            for key, value in flags.items():
                file.write(f"{key}: {value}\n") 



    def load_scene_flags(self, scene_id: int) -> dict[str, bool]:
        """
        Load the flags of the scene with some scene ID

        Parameters:
        scene_id: int - the scene's ID number
        Returns;
        dict[str, bool] - the scene's flags representing completed question sessions
        """
        # Construct the file path
        file_path = os.path.join(self.directory, f"scene_{scene_id}.txt")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Scene file for ID {scene_id} not found.")
        
        # Initialize an empty dictionary to store flags
        flags = {}

        # Read the data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Skip the scene id
            lines.reverse()
            lines.pop()

            for line in lines:
                key, value = line.strip().split(": ")
                value = value == "True"
                flags[key] = value
        
        return flags
            
