# VPR

This is Vagrant Private Repository app.

It's still under development.

### How to Run It

1. Create a virtualenv and activate it.

```bash
python3 -m venv venv

source venv/bin/activate
```
2. Install the requirements.

```bash
pip3 install --upgrade -r requirements.txt
```

3. Apply the database migrations.

```bash
python manage.py migrate
```

4. Run the app.

```bash
python3 manage.py runserver
```