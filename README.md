# Dev-up API

## For test deployment

- There should be the `.config` folder in the project root folder which contains several files & folders such as

```
Project-Root
├── .config
│    ├── env
│    │    └**dev_up.env**
│    ├── ssl
│    │    ├**your_public_key**
│    │    └**your_private_key**
│    └── nginx
│         └**nginx.conf**
├── common
├── dev_up
├── post
├── stubs
├── tests
├── user
│
│   ...
```

### Configurations that should contain
---

- **dev_up.env**
	- [Optional] `DJANGO_SECRET_KEY`
		- A random string
		- ex) ```DJANGO_SECRET_KEY=98xc(!)A*Bhw@Dna89@$(c2)!*da```
	- [Optional] `DJANGO_MODE`
		- Turn on or off debug mode; Debug mode is off when `DJANGO_MODE=production` otherwise it will be off.
		- ex) ```DJANGO_MODE=production```
	- **[Required]** `ALLOWED_HOSTS`
		- Your server domain address is required. If domains are more than one, they are separated by comma.
		- ex) ```ALLOWED_HOSTS=example.com,123.456.789.012```
	- **[Required]** `CORS_ORIGIN_WHITELIST`
		- If your client server is not in the same server, this option is required.
		- ex) ```CORS_ORIGIN_WHITELIST=example.com,123.456.789.012```
	- **[Required]** `EMAIL_HOST`
	- **[Required]** `EMAIL_PORT`
	- **[Required]** `EMAIL_HOST_USER`
	- **[Required]** `EMAIL_HOST_PASSWORD`
	- **[Required]** `POSTGRESQL_HOST`
	- **[Required]** `POSTGRESQL_PORT`
	- **[Required]** `POSTGRESQL_NAME`
	- **[Required]** `POSTGRESQL_USER`
	- **[Required]** `POSTGRESQL_PASSWORD`
	- **[Required]** `GOOGLE_OAUTH_ClIENT_ID`
	- **[Required]** `GOOGLE_OAUTH_SECRET`
	- **[Required]** `GITHUB_OAUTH_CLIENT_ID`
	- **[Required]** `GITHUB_OAUTH_SECRET`
- **nginx.conf**
	- should contains nginx settings such as
	```
    # Indicate web application (dev-up)
    upstream app {
        ip_hash;
        server web:8000;
	}
    
    # Could be optional
    server {
        listen 80;
        server_name your_server_domain;

        # Redirect all traffic to HTTPS
        return 301 https://$host$request_uri;
    }
    
    # Connect nginx server to web application
    server {
        listen 443 ssl;
        server_name your_server_domain;
		
        ssl_certificate /app/ssl/your_public_key;
        ssl_certificate_key /app/ssl/your_private_key;

        location /favicon.ico {
            access_log off;
            log_not_found off;
        }

        location /static/ {
            root /app;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://app/;
        }
    }
    ```
### How to set the server up
---
1. Install docker.

	[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

2. Install docker compose.

	[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

3. Clone this project via GitHub.

	```
	$ git clone https://github.com/devv-up/backend.git
	```

4. Move into the project root folder and type this.
	```
	$ docker-compose up -d --build
	```

5. Enjoy

## Or you can simply access the test server

[https://ops-test.com/](https://ops-test.com/)

## How to use

Check the API manual.
- [http://3.34.46.127:8001/swagger/](http://3.34.46.127:8001/swagger/)