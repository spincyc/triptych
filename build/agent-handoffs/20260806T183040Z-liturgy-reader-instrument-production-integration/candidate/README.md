# Runnable production-integration candidate

From the handoff root run:

```sh
python3 -m http.server 8000
```

Then open:

- Day Read: `http://localhost:8000/candidate/liturgy/day-reader.html?data=/candidate/browse#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=0`
- Day Missal: `http://localhost:8000/candidate/liturgy/day-reader.html?data=/candidate/browse#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=1&ordinary-lang=en&rubrics=1&why=0`
- Propers Read: `http://localhost:8000/candidate/liturgy/propers-reader.html?data=/candidate/browse#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la`
- accepted Day oracle: `http://localhost:8000/candidate/liturgy/reader-visual-reset-day.html?design=instrument&data=/candidate/browse#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mass=pentecost-10&ordinary=1&ordinary-lang=en&rubrics=1&why=0`

The bundle contains only the focused browser assets and data needed for the
governing review states. It is a review candidate, not a public-cutover bundle.
