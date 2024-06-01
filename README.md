### README.md for `live_chat_feature`

# Live Chat Feature

This repository contains the implementation of a live chat feature using Django for the backend and Vue.js for the frontend. The application utilizes WebSockets for real-time communication and integrates with Redis for message brokering.

## Features

- Real-time chat functionality
- User and admin chat roles
- WebSocket implementation for live updates
- Redis for message brokering
- Vue.js frontend with `vue-advanced-chat` library

## Models

### User
- **Attributes**:
  - `email`: Email of the user.
  - `first_name`: First name of the user.
  - `last_name`: Last name of the user.

  **Implementation**: [User Model](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/models/user.py)

### Chat
- **Attributes**:
  - `user`: Foreign key to the User model.
  - `admin`: Foreign key to the User model (admin user).
  - `created_at`: Timestamp when the chat was created.
  - `last_message_timestamp`: Timestamp of the last message.
  - `unread_count`: Count of unread messages.
  - `unread`: Boolean indicating if there are unread messages.

  **Implementation**: [Chat Model](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/models/chat.py)

### Message
- **Attributes**:
  - `chat`: Foreign key to the Chat model.
  - `user`: Foreign key to the User model.
  - `text`: Text of the message.
  - `created_at`: Timestamp when the message was created.

  **Implementation**: [Message Model](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/models/message.py)

## Views

### admin_get_or_create
- **Description**: Retrieves or creates an admin user with a fixed email.
- **Implementation**: [admin_get_or_create](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L9-L19)

### user_get_or_create
- **Description**: Retrieves or creates a user based on the provided email, first name, and last name.
- **Implementation**: [user_get_or_create](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L21-L43)

### chat_list_create
- **Description**: Lists all chats or creates a new chat. Sends an email notification when a new chat is created.
- **Implementation**: [chat_list_create](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L45-L84)

### message_list_create
- **Description**: Lists all messages or creates a new message. Updates the chat's unread count if necessary.
- **Implementation**: [message_list_create](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L86-L119)

### message_list_by_chat_id
- **Description**: Lists all messages for a specific chat by its ID.
- **Implementation**: [message_list_by_chat_id](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L121-L141)

### chat_delete
- **Description**: Deletes a chat by its ID.
- **Implementation**: [chat_delete](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L143-L155)

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Node.js
- npm or yarn
- Redis server

## Installation

### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/carlos18bp/live_chat_feature.git
    cd live_chat_feature
    ```

2. **Install virtualenv**:
    ```bash
    pip install virtualenv
    ```

3. **To create a new virtual env**:
    ```bash
    virtualenv name_virtual_env
    ```

4. **Create virtual env**:
    ```bash
    virtualenv live_chat_feature_env
    ```

5. **Activate virtual env**:
    ```bash
    source live_chat_feature_env/bin/activate
    ```

6. **Create dependencies file**:
    ```bash
    pip freeze > requirements.txt
    ```

7. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

8. **Desactivate virtual env**:
    ```bash
    deactivate
    ```

9. **Set up the database:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

10. **Create fake data for testing:**

    ```bash
    python manage.py create_fake_data
    ```

11. **Delete fake data for testing:**

    ```bash
    python manage.py delete_fake_data
    ```

12. **Install Daphne:**

    Daphne is an HTTP, HTTP2, and WebSocket protocol server for ASGI and ASGI-HTTP, developed as part of the Django Channels project.

    ```bash
    pip install daphne
    ```

12. **Run the Redis server:**

    Ensure you have Redis installed and running. You can install it using:

    ```bash
    sudo apt-get install redis-server
    sudo service redis-server start
    ```

13. **Run the development server using Daphne:**

    ```bash
    daphne -p 8000 live_chat_project.asgi:application
    ```

### Backend Configuration

- **Django Channels Configuration:**
  Ensure `channels` and `channels_redis` are installed and configured in your `settings.py`.

    ```python
    INSTALLED_APPS = [
        ...
        'channels',
    ]

    ASGI_APPLICATION = 'live_chat_project.asgi.application'

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
        },
    }
    ```

- **ASGI Configuration:**
  Update your `asgi.py` to include WebSocket routing:

    ```python
    import os
    from django.core.asgi import get_asgi_application
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter
    import live_chat_app.routing

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_chat_project.settings')

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                live_chat_app.routing.websocket_urlpatterns
            )
        ),
    })
    ```

- **WSGI Configuration:**
  Ensure your `wsgi.py` is set up correctly:

    ```python
    import os
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_chat_project.settings')

    application = get_wsgi_application()
    ```

- **WebSocket Routing:**
  Define WebSocket routing in `live_chat_app/routing.py`:

    ```python
    from django.urls import path
    from live_chat_app.web_socket.consumers import ChatConsumer

    websocket_urlpatterns = [
        path('ws/chat/', ChatConsumer.as_asgi()),
    ]
    ```

### Frontend Setup

1. **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2. **Install the dependencies:**

    ```bash
    npm install
    # or
    yarn install
    ```

3. **Configure `vite.config.js` for `vue-advanced-chat` and socket:**

    ```javascript
    import { defineConfig } from 'vite';
    import vue from '@vitejs/plugin-vue';
    import { fileURLToPath, URL } from 'url';

    // https://vitejs.dev/config/
    export default defineConfig({
    server: {
        proxy: {
        '/api': {
            target: 'http://127.0.0.1:8000/',
            changeOrigin: true,
            secure: false,
            rewrite: (path) => path.replace(/^\/api/, ''),
        },
        '/ws': {  // Add support for WebSockets
            target: 'ws://127.0.0.1:8000/',
            ws: true,
            changeOrigin: true,
            secure: false,
        },
        },
    },
    plugins: [
        vue({
        template: {
            compilerOptions: {
            isCustomElement: tagName => {
                return tagName === 'vue-advanced-chat' || tagName === 'emoji-picker'
            }
            }
        }
        }),
    ],
    resolve: {
        alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    }
    });
    ```

4. **Run the frontend development server:**

    ```bash
    npm run dev
    # or
    yarn dev
    ```

5. **Frontend Socket Configuration:**
  Ensure your `frontend/src/store/socket.js` is correctly set up for WebSockets.

    **Implementation**: [socket.js](https://github.com/carlos18bp/live_chat_feature/blob/master/frontend/src/store/socket.js)

### Email Notification

An email notification is sent when a new chat is created. This is implemented in `live_chat_app/views/chat.py`:

**Implementation**: [Email Notification](https://github.com/carlos18bp/live_chat_feature/blob/master/live_chat_app/views/chat.py#L109-L112)

## Usage

After setting up the backend and frontend, you can start the development servers and access the live chat application in your browser.

- Admin Live Chat: [http://localhost:5173/admin_live_chat](http://localhost:5173/admin_live_chat)
- User Live Chat: [http://localhost:5173/](http://localhost:5173/)

## Acknowledgements

- [Vue Advanced Chat](https://github.com/advanced-chat/vue-advanced-chat)
- [Django Channels](https://channels.readthedocs.io/en/stable/)
- [Redis](https://redis.io/)
