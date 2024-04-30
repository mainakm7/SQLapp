# To-do_list_app

## Description
To-do_list_app is a simple application designed to help users store and manage their to-do events. It utilizes a SQL database to store to-do items and incorporates user authentication features. Users can create a profile, log in securely, and then add, modify, or delete their to-do items within the app. The application provides REST APIs for performing CRUD (Create, Read, Update, Delete) operations on the to-do items, making it easy to integrate with other systems or extend its functionality.

## Features
- User authentication system: Allows users to create accounts and securely log in.
- To-do management: Users can add, update, delete, and view their to-do items.
- REST APIs: Provides endpoints for performing CRUD operations on to-do items, facilitating integration with other systems.
- Relative module imports: Utilizes relative imports for compatibility with pytest, ensuring smooth testing procedures.

## Installation
1. Clone the repository: `https://github.com/mainakm7/To-do_list_app.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Ensure you have SQLite3 and MySQL 5.6 installed and running on your system.
2. Run the application from the root folder outside the app package, e.g., `root_folder/To-do_list_app`.
3. Access the application through your preferred web browser or API client.
4. Create a user profile and log in to start managing your to-do items.

## Database
- The application supports any SQL database options: SQLite3 and MySQL:5.6 were tested.
- Choose the appropriate database configuration in the application settings or environment variables.
- Ensure the database server is running and accessible before running the application.

## Development
- This application was developed using FastAPI for building REST APIs.
- Pytest is used for testing, with relative module imports for compatibility.
- Contributions and feedback are welcome. Feel free to submit pull requests or raise issues on the GitHub repository.

## Contributors
- Mainak Mustafi

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


