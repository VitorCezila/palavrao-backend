# Wordify backend

Serverless backend for [Wordify](https://play.google.com/store/apps/details?id=com.cezila.palavreando), a daily word game for Android. It serves the daily word and creates and resolves friend challenges.

Built with AWS SAM: API Gateway, Lambda (Python 3.13) and DynamoDB, deployed to separate `dev` and `prod` stacks by GitHub Actions.

---

## Architecture

```
Android app ──(x-api-key)──► API Gateway ──► Lambda functions ──► DynamoDB
                                                  │
                                                  └── shared Lambda layer (palavrao)
```

| Endpoint | Method | Lambda | What it does |
| --- | --- | --- | --- |
| `/daily-word` | GET | `GetDailyWord` | Returns today's word (Brazil time). Picks one at random from a 5-letter Portuguese word list the first time it is requested each day, then stores it so every player gets the same word. |
| `/word-challenge` | POST | `PostCreateWordChallenge` | Creates a friend challenge and returns a share code. |
| `/word-challenge/{code}` | GET | `GetChallengeByCode` | Looks up a challenge by its code. |

All endpoints require an API key (`ApiKeyRequired` on API Gateway).

---

## Code structure

Business logic lives in a shared Lambda layer, split into interfaces and implementations so each Lambda handler stays thin.

```
src/lambda/
├── functions/api/          # One folder per Lambda handler
└── layers/main/palavrao/
    ├── interfaces/         # Service, DAO, repository and request-context contracts
    ├── implementations/    # DynamoDB DAOs and converters, services, file word repository
    ├── model/              # Domain models (DailyWord, WordChallenge, ...)
    ├── dto/                # Response shapes
    └── requests/           # Error handling and HTTP response helpers
```

---

## Deployment

`.github/workflows/deploy.yml` builds and deploys with SAM on every push:

- `develop` → `palavrao-stack-dev`
- `main` → `palavrao-stack-prod`

AWS access uses GitHub OIDC (`role-to-assume`), so no long-lived AWS keys are stored in the repository or in GitHub Secrets.

---

## Running locally

Requires the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html), Docker and Python 3.13.

```bash
sam build --use-container
sam local start-api
```

To deploy to your own account:

```bash
sam deploy --config-env dev
```

---

## License

MIT
