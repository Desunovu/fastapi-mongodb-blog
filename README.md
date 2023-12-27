# Blog development using Fast API, Vue.js and MongoDB

## Introduction

This project is an educational project for developing a blog using Fast API, Vue.js and MongoDB. The main goal of the project is to demonstrate the use of a NoSQL database and asynchronous CRUD operations.
![homepage](/demo-assets/homepage.png)
[The rest of the demo screenshots](demo-assets/screenshots.md)

## Technology Stack

- **Programming Languages**: Python, TypeScript/JavaScript
- **Backend Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: MongoDB (used with  [Beanie ODM](https://beanie-odm.dev/))
- **Frontend Web Framework**: Vue.js (with [Quasar](https://quasar.dev/), [Pinia](https://pinia.vuejs.org/), [OpenAPI Typescript Codegen](https://github.com/ferdikoomen/openapi-typescript-codegen))
- **Honorable mention**:  OAuth 2.0 JWT Bearer Flow, Nginx, Chat completions API

## Project Functionality
1. **Registration and Authentication**: Users can register and authenticate using OAuth 2.0 JWT.
2. **Profile Management**: Users can manage their profiles, including changing passwords and updating information. Administrators can also manage users.
3. **Blog Management**: Authors can create, edit, and delete blog articles.
4. **Viewing Articles**: Articles can be viewed as a list and in detail. Pagination and sorting are supported for displaying a large number of articles.
5. **Tags and Filters**: Articles can be filtered by tags, and users can add tags to articles.
6. **Search**: Search for articles using keywords.
7. **Comments**: Users can add comments and reply to them.
8. **Article Generation**: Admins can generate articles using the OpenAI chat completion API.


## Installation and Local Setup
To run this project locally, you can use Docker Compose. Make sure you have Docker and Docker Compose installed on your system.

1. Clone the repository:

   ```bash
   git clone https://github.com/Desunovu/fastapi-vue-blog.git
   cd fastapi-vue-blog
   ```
   

2. Rename the example environment files located in the project's root directory:
   - Rename `.env.production.example` to `.env.production`
   - Rename `.env.development.example` to `.env.development`


3. Open the newly created .env.production and .env.development files using a text editor. In these files, you can customize the variables according to your preferences. For example:

   ```dotenv
   FASTAPI_SECRET_KEY=mysecretkey
   FASTAPI_CHATGPT_ALTERNATIVE_BASE=https://neuroapi.host/v1
   FASTAPI_CHATGPT_API_KEY=someapikey
   FASTAPI_CREATE_TEST_USERS=true
   FASTAPI_LOGGING_LEVEL=debug
   ```


4. Build and start the application containers using Docker Compose. You can specify profiles using the --profile argument as follows:
   - To deploy the full application stack, use:
   ```bash
   docker-compose --profile full-deploy up --build
   ```
   - To run only the FastAPI and MongoDB containers, use:
   ```bash
   docker-compose --profile backend-only up --build
   ```
   - To run only the MongoDB container, use:
   ```bash
   docker-compose --profile mongodb-only up --build
   ```

This command will download the necessary Docker images, build the application, and start the containers.

## Accessing the Application
- Vue App: http://localhost:8080
- API Documentation: http://localhost:8000/docs

## License

This project is distributed under the [MIT License](LICENSE).