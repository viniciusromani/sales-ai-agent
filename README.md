## Description

AI Sales Agent is a modular and extensible system designed to assist sales teams by autonomously handling prospect conversations. Upon receiving a new message in an ongoing conversation, the agent leverages context, retrieval-augmented generation (RAG), and integrated tools to generate an informed and context-aware response.

This project demonstrates the usage of LLMs through OpenAI’s official SDK, integrates a vector database (Qdrant) for semantic retrieval, and follows best practices in API design, software modularity, and containerization. It is designed with future scalability and production-readiness in mind.


### Built With

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [OpenAI](https://platform.openai.com/docs/libraries)
* [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
* [Qdrant](https://qdrant.tech/)
* [Docker](https://www.docker.com/)

### System Architecture

![Architecture](assets/architecture.jpg)

## Getting Started

The following instructions get you a local running copy of the application.

### Prerequisites

* Docker
* Python (if you want to run the agent in a different environment than qdrant)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/viniciusromani/sales-ai-agent.git
   ```

2. Create a `.env` file on project's root folder with the following variables:
   ```sh
    OPENAI_API_KEY={{Your OpenAI Key}}
    QDRANT_HOST={{Qdrant Host}}
   ```
Obs. If you are using docker to run, `QDRANT_HOST` will be `qdrant` since it is the service name on `docker-compose.yml` file.

3. Run `docker-compose`
   ```sh
   docker-compose up
   ```

### Installation (without docker)

1. Clone the repo
   ```sh
   git clone https://github.com/viniciusromani/sales-ai-agent.git
   ```

2. Create a `.env` file on project's root folder with the following variables:
   ```sh
    OPENAI_API_KEY={{Your OpenAI Key}}
    QDRANT_HOST={{Qdrant Host}}
   ```
Obs. If you follow step #3 to get a local qdrant running. Your `QDRANT_HOST` will be `http://localhost:6333` unless you changed port value.

3. Follow [these instructions](https://qdrant.tech/documentation/quickstart/) to get you qdrant running
Obs. You might access `http://localhost:6333/dashboard` to check qdrant UI and your local collections.

4. (Recommended) Create a [virtual environment](https://docs.python.org/pt-br/dev/library/venv.html) and activate it.

5. Install dependencies
   ```sh
    pip install -r requirements.txt
   ```

### Tests

1. Run tests
   ```sh
   pytest
   ```
2. Get unit tests coverage
   ```sh
   pytest --cov-report html
   ```
Obs. It will generate a folder `htmlcov/` on project root. Inside this folder there is a `index.html` file that you can open in any browser to check coverage in a human readable way

<!-- ROADMAP -->
## Roadmap

- [ ] Implement [eval](https://platform.openai.com/docs/guides/evals) to follow how the agent is performing
- [ ] Create agent evaluation pipeline in order to keep track of its performance
- [ ] Create a data ingestion pipeline that is not attached to application startup
- [ ] Move error handling exclusively to routers
- [ ] Improve logging

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an incredible place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- CONTACT -->
## Contact

Vinicius Romani - vn.romani@gmail.com