#### Description
Here you can see a test task for a headhunter from Avalon Chase.

#### Required software
Make sure you have installed docker, docker-compose and curl.

#### Installing
- Clone the repository
`git clone https://github.com/missterr/test-task-foreign-exchange.git`
- Get into the root directory
`cd test-task-foreign-exchange`
- Build images
`docker-compose build`
- Run docker containers
`docker-compose up`

#### Making requests
- The first task is just getting currency list
`curl --user test@test.com:123Qwertyu http://127.0.0.1:8010/currencies/`
- The second API returns the latest rate and average of volume for the last 10 days
`curl --user test@test.com:123Qwertyu http://127.0.0.1:8010/currencies/2/rate/`
- The third required demonstration is paginated request
`curl --user test@test.com:123Qwertyu http://127.0.0.1:8010/currencies/?limit=2&offset=2`

#### Prevension
