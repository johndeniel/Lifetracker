# Lifetracker

Lifetracker is a web application built with FastAPI. It provides an intuitive interface for users to input their birth date and instantly see how many days they have been alive. Lifetracker has been Dockerized for effortless deployment, and its Docker image is readily available on [Docker Hub](https://hub.docker.com/r/johndeniel/lifetracker/tags).

To run Lifetracker using Docker, execute this command in your terminal:

```bash
docker run -d -it --name lifetracker -p 7860:7860 johndeniel/lifetracker:build-v1.052
```

## Features

- **FastAPI Integration**: Lifetracker utilizes FastAPI, a modern Python web framework known for its speed and efficiency, to power its backend functionality.

- **Pre-commit Hooks**: Lifetracker integrates pre-commit hooks for code quality checks, ensuring consistent and clean code before commits.

- **Automated Dockerization**: Lifetracker includes a GitHub Action workflow for Dockerizing the FastAPI application, streamlining the deployment process with automated containerization.

- **Hugging Face Platform Integration**: Lifetracker seamlessly integrates with the Hugging Face Platform, offering access to the live instance on [Hugging Face Spaces](https://huggingface.co/spaces/johndeniel/Lifetracker).

---

Lifetracker demonstrates the utilization of cutting-edge technologies like FastAPI, Docker, GitHub Actions, and the Hugging Face Platform, offering developers an efficient development experience.