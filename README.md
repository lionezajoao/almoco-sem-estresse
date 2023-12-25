# Menu Website

- Project structure

```
root/
├── server/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_endpoints.py
│   ├── .env
│   ├── requirements.txt
│   └── Dockerfile
├── client/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   ├── .env
│   ├── package.json
│   └── Dockerfile
├── .gitignore
├── README.md
└── ...
```
 