from app.users.users_apis import users
from app.users.educations_apis import educations
from app.users.health_apis import health
from app.users.career_apis import career
from app.users.docs_apis import docs

api_routes=[
    users.routes,
    educations.routes,
    health.routes,
    career.routes,
    docs.routes
]