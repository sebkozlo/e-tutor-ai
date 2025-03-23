# e-Tutor AI

1. Sklonuj repozytorium: 

```git clone ```

2. W katalogu root (w katalogu root znajduje się plik ```manage.py```)utwórz plik ```.env``` kopiuj schemat z ```.env.example``` uzupełnij dane (klucze API, etc)


3. Zbuduj obrazy Dockera:

```docker-compose build```

4. Uruchom kontenery:

```docker-compose up```

Aplikacja będzie dostępna pod adresem: http://localhost:8000

Dokumentacja API http://localhost:8000/api/docs
