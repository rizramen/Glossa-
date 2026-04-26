# Glossa

Glossa is a server-rendered Django web application for personal vocabulary learning. Users can register, log in, create their own dictionaries, and add words with definitions and language tags. The project also contains early scaffolding for quizzes, friendships, and a "word of the day" feature.

## What the project currently does

Implemented:

- User registration, login, and logout
- Per-user dictionary list
- Dictionary creation
- Dictionary detail pages
- Adding words to a dictionary
- Basic navigation shared through `templates/base.html`

Present but mostly unfinished:

- Quiz app: models exist, but views/templates are placeholders
- Friends app: `Friendship` model exists, but UI is static
- Word of the day app: routes and templates exist, but no active model-backed logic
- Dashboard/account pages: template stubs only

## Tech stack

- Python
- Django
- SQLite
- Django class-based views
- Django templates

## Project structure

```text
Glossa/         Project settings and root URL configuration
pages/          Landing page and dashboard pages
users/          Authentication pages and user profile model
dictionary/     Core dictionary and word management flow
quiz/           Quiz models and placeholder quiz pages
friends/        Friendship model and placeholder page
wordofday/      Word-of-the-day placeholder pages
templates/      Shared base template
db.sqlite3      Local SQLite database
manage.py       Django management entry point
```

## Main apps

### `dictionary`

This is the most complete part of the application.

- `Dictionary` belongs to a Django `User`
- `Word` belongs to a `Dictionary`
- Logged-in users only see their own dictionaries
- Logged-in users can only open and modify dictionaries they own
- Adding a word is scoped to a specific dictionary

Relevant routes:

- `/dictionary/`
- `/dictionary/list/`
- `/dictionary/create/`
- `/dictionary/<id>/`
- `/dictionary/<id>/add-word/`

### `users`

The project uses Django’s built-in authentication system.

- Login uses Django `LoginView`
- Registration uses Django `UserCreationForm`
- Logout uses Django `LogoutView`
- There is also a `UserProfile` model for extra user data such as preferred language, age, and phone number

Important note: the project does not use a custom user model. `users/models.py` defines a separate `UserProfile` linked with `OneToOneField`.

### `quiz`

The app defines:

- `Quiz`
- `QuizResult`

These models suggest the intended flow is to run quizzes against a selected dictionary and store correctness per word. However, the current views are only static `TemplateView`s, so quiz behavior is not implemented yet.

### `friends`

The app defines a `Friendship` model with `pending` and `accepted` states, but the page at `/friends/` is currently only a static template.

### `wordofday`

This app contains routes for:

- `/wordofday/`
- `/wordofday/word-of-day/`
- `/wordofday/admin/word-of-day/`

At the moment, it only renders placeholder templates. `wordofday/models.py` is empty, so there is no persisted "word of the day" feature yet.

## Routing overview

Root routing is defined in `Glossa/urls.py`:

- `/admin/`
- `/`
- `/users/`
- `/dictionary/`
- `/quiz/`
- `/friends/`
- `/wordofday/`

## Data model summary

Core entities:

- `User` from Django auth
- `UserProfile` linked one-to-one with `User`
- `Dictionary` linked many-to-one to `User`
- `Word` linked many-to-one to `Dictionary`
- `Quiz` linked to `User` and `Dictionary`
- `QuizResult` linked to `Quiz` and `Word`
- `Friendship` linking one user to another with a status

## Setup

The repository currently does not include a dependency file such as `requirements.txt` or `pyproject.toml`, so setup has to be done manually.

Example local setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "Django>=6,<7"
python3 manage.py migrate
python3 manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/`

## Development notes

- Database: SQLite (`db.sqlite3`)
- Templates are server-rendered and mostly minimal HTML
- Authentication-protected dictionary pages use `LoginRequiredMixin`
- The repository includes migrations for the existing apps

