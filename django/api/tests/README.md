# Django Test Suite

## Writing Tests

Django uses the standard Python assert methods:

- assertEqual(a, b)
- assertNotEqual(a, b)
- assertTrue(x)
- assertFalse(x)
- assertIs(a, b)
- assertIsNot(a, b)
- assertIsNone(x)
- assertIsNotNone(x)
- assertIn(a, b)
- assertNotIn(a, b)
- assertIsInstance(a, b)
- assertNotIsInstance(a, b)

## Running Tests in Docker

Log into the API docker container and run the following command:

```bash
./manage.py test
```

uu
