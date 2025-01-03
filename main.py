import json
import random
import pyfiglet


class InteractiveStoryBuilder:
    def __init__(self):
        self.story = {}
        self.current_node = "start"
        self.saved_file = "story_save.json"
        self.theme = None

    def create_default_story(self):
        """Create a default story structure."""
        self.story = {
            "start": {
                "description": "You wake up in a mysterious forest. There's a path to the north and south.",
                "options": ["Go North", "Go South"],
                "next_nodes": {"Go North": "cabin", "Go South": "river"}
            },
            "cabin": {
                "description": "You find a small cabin in the woods. The door creaks open as you approach.",
                "options": ["Enter the cabin", "Go back"],
                "next_nodes": {"Enter the cabin": "treasure", "Go back": "start"}
            },
            "river": {
                "description": "You hear the sound of rushing water. A river lies ahead.",
                "options": ["Cross the river", "Go back"],
                "next_nodes": {"Cross the river": "danger", "Go back": "start"}
            },
            "treasure": {
                "description": "Inside the cabin, you discover a chest filled with gold! You win!",
                "options": ["Restart"],
                "next_nodes": {"Restart": "start"}
            },
            "danger": {
                "description": "A wild beast attacks you at the riverbank. You have lost the game.",
                "options": ["Restart"],
                "next_nodes": {"Restart": "start"}
            }
        }

    def load_story(self):
        """Load a saved story structure."""
        try:
            with open(self.saved_file, 'r') as f:
                data = json.load(f)
                self.story = data['story']
                self.current_node = data['current_node']
                print("Progress successfully loaded!")
        except FileNotFoundError:
            print("No saved progress found. Starting a new story.")

    def save_story(self):
        """Save the current story progress."""
        with open(self.saved_file, 'w') as f:
            json.dump({"story": self.story, "current_node": self.current_node}, f)
        print("Progress saved successfully!")

    def display_ascii_art(self, text):
        """Display ASCII art for the current theme."""
        if self.theme:
            print(pyfiglet.figlet_format(text))
        else:
            print(f"** {text} **")

    def play(self):
        """Main game loop."""
        while True:
            node = self.story[self.current_node]
            self.display_ascii_art(node["description"])

            if "options" in node and node["options"]:
                print("\nWhat would you like to do?")
                for i, option in enumerate(node["options"], 1):
                    print(f"{i}. {option}")

                try:
                    choice = int(input("\nEnter your choice (number): "))
                    selected_option = node["options"][choice - 1]
                    self.current_node = node["next_nodes"][selected_option]
                except (ValueError, IndexError):
                    print("Invalid choice. Please try again.")
            else:
                print("No further options available. The story ends here.")
                break

            # Random events
            if random.random() < 0.2:  # 20% chance of a random event
                print("A random event occurs! Something unexpected happens...")
                event_outcome = random.choice(["You found a hidden treasure!", "You encountered a friendly traveler!"])
                print(event_outcome)

            # Save option
            save = input("\nWould you like to save your progress? (yes/no): ").strip().lower()
            if save == "yes":
                self.save_story()

    def set_theme(self):
        """Set the ASCII art theme."""
        themes = ["Fantasy", "Sci-Fi", "Mystery"]
        print("\nAvailable Themes:")
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme}")

        try:
            choice = int(input("\nChoose a theme (number): "))
            self.theme = themes[choice - 1]
            print(f"Theme set to {self.theme}.")
        except (ValueError, IndexError):
            print("Invalid choice. Default theme will be used.")

    def add_custom_node(self):
        """Allow users to add their own story nodes."""
        node_name = input("Enter the name of the new node: ").strip()
        description = input("Enter the description of the new node: ").strip()
        options = input("Enter options (comma-separated): ").strip().split(",")
        next_nodes = {}

        for option in options:
            target_node = input(f"Where does '{option.strip()}' lead? ").strip()
            next_nodes[option.strip()] = target_node

        self.story[node_name] = {
            "description": description,
            "options": options,
            "next_nodes": next_nodes
        }
        print(f"Node '{node_name}' added successfully!")

    def menu(self):
        """Main menu for the story builder."""
        while True:
            print("\n--- Interactive Story Builder ---")
            print("1. Play Story")
            print("2. Add Custom Node")
            print("3. Load Saved Progress")
            print("4. Set Theme")
            print("5. Exit")

            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_custom_node()
                elif choice == 3:
                    self.load_story()
                elif choice == 4:
                    self.set_theme()
                elif choice == 5:
                    print("Exiting the Story Builder. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

# Run the program
if __name__ == "__main__":
    builder = InteractiveStoryBuilder()
    builder.create_default_story()
    builder.menu()
