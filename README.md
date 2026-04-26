# Glossa

Glossa is a server-rendered Django vocabulary-learning app. Users can register, create personal dictionaries, add words and definitions, and quiz themselves on saved vocabulary.

## Current Features

- User registration, login, and logout
- Per-user dictionaries
- Dictionary creation with a chosen language
- A preset list of 20 common learning languages plus a custom language option
- Dictionary detail pages
- Adding words to a dictionary without re-selecting the language
- Deleting dictionaries with a confirmation screen
- Quiz flow with dictionary selection, multiple-choice questions, and result pages
- Shared navigation and styling through base templates and a central stylesheet

## Still In Progress

- Friends page is only a placeholder
- Word-of-the-day pages are still placeholders
- Dashboard and account pages are minimal

## Tech Stack

- Python
- Django
- SQLite for local development
- PostgreSQL-ready production configuration

## Project Structure

```text
Glossa/         Project settings and root URL configuration
pages/          Landing page and dashboard pages
users/          Authentication pages and user profile model
dictionary/     Dictionary creation, word management, and delete flow
quiz/           Quiz start, question, and results flow
friends/        Placeholder friends page
wordofday/      Placeholder word-of-the-day pages
static/         Shared CSS
templates/      Shared base template
manage.py       Django management entry point
render.yaml     Render deployment blueprint
build.sh        Render build script
```

## Main Apps

### `dictionary`

- `Dictionary` belongs to a Django `User`
- Each dictionary has one language
- `Word` belongs to a `Dictionary`
- Logged-in users only see and modify their own dictionaries
- Users can create, open, update by adding words, and delete their dictionaries

Relevant routes:

- `/dictionary/`
- `/dictionary/list/`
- `/dictionary/create/`
- `/dictionary/<id>/`
- `/dictionary/<id>/add-word/`
- `/dictionary/<id>/delete/`

### `quiz`

- Users choose one of their dictionaries to start a quiz
- Each question shows a word and multiple definition choices
- Results are stored in `Quiz` and `QuizResult`
- Users can review recent quiz attempts

Relevant routes:

- `/quiz/`
- `/quiz/start/`
- `/quiz/question/`
- `/quiz/result/<quiz_id>/`

### `users`

- Login uses Django `LoginView`
- Registration uses Django `UserCreationForm`
- Logout uses Django `LogoutView`
- `UserProfile` stores extra optional user information

### `friends`

- The route exists and renders a placeholder “coming soon” page

### `wordofday`

- Routes and templates exist, but no active model-backed feature is implemented yet

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/`

## Running Tests

```bash
python manage.py test
```

## Deployment

The repository is prepared for deployment on Render.

Relevant files:

- [render.yaml](./render.yaml)
- [build.sh](./build.sh)
- [requirements.txt](./requirements.txt)

Production-related settings already included:

- `gunicorn`
- `whitenoise`
- `dj-database-url`
- PostgreSQL-ready `DATABASE_URL` support
- `STATIC_ROOT` and collected static file support
- secure production settings when `DJANGO_DEBUG=False`



## Development Notes

- Local database: `db.sqlite3`
- Shared CSS lives in `static/css/style.css`
- Shared base HTML lives in `templates/base.html`
- Dictionary and quiz pages rely on `LoginRequiredMixin` where appropriate
