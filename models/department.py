class Department:
    """Represents a hospital department."""

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def display_department_info(self):
        """Display department information."""

        print("\n--- Department Information ---")
        print(f"Department Name: {self.name}")
        print(f"Description: {self.description}")


# Test the Department class
if __name__ == "__main__":

    department = Department(
        name="Cardiology",
        description="Department for heart-related treatments"
    )

    department.display_department_info()
    