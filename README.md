
## Installation

```bash
touch .env
echo "ELASTIC_PASSWORD=LpsPWVK9OpdESajV5hKB" >> .env
pip install -r requirements.txt

```

## Usage for development

```
uvicorn main:app --port 7004 --reload 
```
```