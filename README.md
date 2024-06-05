# XBOT - Telegram AI Bot for Post Generation

XBOT is a Telegram bot designed to assist users in generating, editing, and enhancing posts. The bot leverages advanced AI models from OpenAI, including GPT-3.5, DALL-E 3, and Whisper, to create textual content, generate images, and transcribe audio, respectively.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Text Generation:** Create engaging posts using OpenAI's GPT-3.5.
- **Image Generation:** Generate relevant images with DALL-E 3.
- **Audio Transcription:** Convert audio messages to text using Whisper.
- **Telegram Integration:** Seamless integration with Telegram API.
- **User and Post Management:** Store and manage users and posts with SQLAlchemy.

## Installation

### Prerequisites

- Python 3.12.2
- Docker (optional, for deployment)
- PostgreSQL (recommended for production)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/lezhocheck/telegram-ai-post-generator
    cd telegram-ai-post-generator
    ```

2. Install dependencies:
    ```bash
    poetry install
    ```

3. Set up environment variables:
    - Copy the example environments and fill in your configuration details:
    ```bash
    POSTGRES_USER=<your username>
    POSTGRES_PASSWORD=<your password>
    DB=postgresql://<your username>:<your password>@postgres:5432/postgres
    SERVICE_HOST=<public host url, you can use ngrok to obtain one>
    BOT_TOKEN=<your bot token obtained from Telegram Bot Father>
    TELEGRAM_SECRET=<your Telegram secret token>
    OPENAI_KEY=<your OpenAI API token>
    TEST_MODE=false
    ```

## Usage

### Running Locally

1. Activate the virtual environment:
    ```bash
    poetry shell
    ```

2. Start the FastAPI server & PostgreSQL containers:
    ```bash
    docker compose up --build
    ```

3. Start ngrok for local development:
    ```bash
    ngrok http 8000
    ```

### Telegram Commands

- `/start` - Start interacting with the bot.
- `/post` - Create a new post.

## Configuration

- **FastAPI:** Main application framework.
- **SQLAlchemy:** ORM for database management.
- **aiogram:** Integration with Telegram API.
- **OpenAI API:** For text, image, and audio processing.

Ensure to configure your environment variables in the `.env` file, including API keys and database connection details.

## Testing

### Running Tests

1. Run unit and integration tests using pytest:
    ```bash
    poetry run pytest
    ```

### Test Structure

- **Tests:** Located in `tests/`.

## Deployment

### AWS Deployment

The application can be deployed to AWS using services like ECR (Elastic Container Registry) and EKS (Elastic Kubernetes Service) for container management and orchestration. The modular architecture allows easy scaling and management in a cloud environment.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using XBOT! If you have any questions or need further assistance, feel free to open an issue or contact the maintainers.