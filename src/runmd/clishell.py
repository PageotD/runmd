import cmd

from . import __version__
from .config import get_configuration
from .process import list_command, process_markdown_files, run_command, show_command


class RunMDShell(cmd.Cmd):
    intro = f"Welcome to the RunMD {__version__} CLI shell. Type help or ? to list commands.\n"
    prompt = "\33[0;33mrunmd>\33[0;0m "
    configuration = get_configuration()
    blocklist = process_markdown_files(None, configuration)

    def do_list(self, arg):
        """List all code block names along with their language."""
        # print("Listing code blocks...")
        list_command(self.blocklist, None)
        # Implement your actual list command logic here

    def do_run(self, arg):
        """Run a specific code block."""
        print(f"Running code block: {arg}")
        # Implement your actual run command logic here

    def do_show(self, arg):
        """Show the content of a specific code block."""
        print(f"Showing code block: {arg}")
        # Implement your actual show command logic here

    def do_exit(self, arg):
        """Exit the RunMD shell."""
        print("Exiting...")
        return True  # Returning True exits the shell

    def do_EOF(self, line):
        """Handle EOF (Ctrl+D) to exit the shell."""
        print("Exiting...")
        return True  # Returning True exits the shell

    def postloop(self):
        """Clean up after the shell exits."""
        print("Shell exited.")


def main():
    RunMDShell().cmdloop()
