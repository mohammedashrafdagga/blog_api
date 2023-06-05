### Welcome to BlogAPI Building by FastAPI!

Hi! I'm Building Blog Api using Fastapi Framework.
The Features is allow to user to create account and Login into Blog to see post in blog and comment it.

| METHOD| ROUTE | FUNCTIONALITY | ACCESS |
|----------|----------|----------|----------|
| *POST*  | ```api/auth/register/```   | Create Account   | All User   |
|  *POST*  | ```api/auth/login/```   | Login   | All User  |
| *GET*   | ```api/post/```   | List all Post   | All User|
| *GET*   | ```api/post/{post_slug}/```   | Detail for Post Item| All User|
| *POST*   | ```api/post/```   | Create New Post   | Superuser   |
| *PUT*   | ```api/post/update/{post_slug}/```   | Update Post Item | Superuser   |
| *DELETE*   | ```api/post/delete/{post_slug}/```   | Delete Post item   | Superuser   |
| *POST*   | ```api/comment/post/{post_slug}/add/```   | Add Comment for Post item | All User |
| *PUT*   | ```api/comment/update/{comment_id}/```   | Update Comment Item | All User |
| *DELETE*   | ```api/comment/delete/{comment_id}/```   | Delete Comment Item  | All User |
