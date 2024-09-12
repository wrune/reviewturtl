# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app/reviewturtl

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/reviewturtl/

# Install Poetry
RUN pip install poetry

# Copy the reviewturtl directory to the container
COPY reviewturtl /app/reviewturtl/
COPY src/db /app/reviewturtl/db

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi  

# Expose the port the app runs on
EXPOSE 80

# Change Workdir
WORKDIR /app/
# Run the application
CMD ["sh", "-c", "cd reviewturtl/db && prisma generate && cd ../../ && uvicorn reviewturtl.api.api:app --host 0.0.0.0 --port 80 --log-level info --timeout-keep-alive 65"]