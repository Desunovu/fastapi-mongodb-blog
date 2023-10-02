# Blog development using Fast API, Vue.js and MongoDB

## Introduction

This project is an educational project for developing a blog using Fast API, Vue.js and MongoDB. The main goal of the project is to demonstrate the use of a NoSQL database and asynchronous CRUD operations.

## Technology Stack

- **Programming Languages**: Python, TypeScript/JavaScript
- **Backend Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MongoDB (used with  [Beanie ODM](https://beanie-odm.dev/))
- **Frontend Web Framework**: Vue.js (with [Quasar](https://quasar.dev/), [Pinia](https://pinia.vuejs.org/), [OpenAPI Typescript Codegen](https://github.com/ferdikoomen/openapi-typescript-codegen))
- **Honorable mention**:  OAuth 2.0 JWT Bearer Flow, Nginx

## Project Functionality
1. **Registration and Authentication**: Users can register and authenticate using OAuth 2.0 JWT.
2. **Profile Management**: Users can manage their profiles, including changing passwords and updating information. Administrators can also manage users.
3. **Blog Management**: Users can create, edit, and delete blog articles.
4. **Viewing Articles**: Articles can be viewed as a list and in detail. Pagination and sorting are supported for displaying a large number of articles.
5. **Tags and Filters**: Articles can be filtered by tags, and users can add tags to articles.
6. **Search**: Search for articles using keywords.
7. **Comments**: Users can add comments and reply to them.


## Installation and Local Setup
To run this project locally, you can use Docker Compose. Make sure you have Docker and Docker Compose installed on your system.

1. Clone the repository:

   ```bash
   git clone https://github.com/Desunovu/fastapi-vue-blog.git
   cd fastapi-vue-blog
   ```
2. Open the `.env.production` file located in the project's root directory using a text editor. Set the `SECRET_KEY` variable in this file to a secure secret key for your application. For example:

   ```dotenv
   SECRET_KEY=mysecretkey
   ```
   Ensure that the SECRET_KEY value is kept secret and not shared publicly.


3. Build and start the application containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
   This command will download the necessary Docker images, build the application, and start the containers.

## Accessing the Application
- Vue App: http://localhost:8080
- API Documentation: http://localhost:8000/docs

## License

This project is distributed under the [MIT License](LICENSE).