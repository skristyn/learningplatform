# frontend

## Quick guide to important files/folders

```
|--src
    |--components <--- plug and play components
    |--layouts <--- standard layouts for different pages
    |--router <--- lists URL paths for pages
    |--store <--- global shared state
    |--types <--- available, custom TypeScript types
    |--views <--- site pages
    |--App.vue <--- put global styles here, otherwise put scoped styles in the views/components
```

### Available Vue features

This project was set up to support the following features:

- TypeScript
- Progressive Web App (PWA) Support
- Vue Router
- Vuex state management
- Prettier code formatter support

## Project setup

### run this before the first time you run the app

```
npm install
```

### Compiles and hot-reloads for development (i.e., run the app)

```
npm run serve
```

## Misc.

### Compiles and minifies for production

```
npm run build
```

Built files are placed in `./dist/production`.

### Compiles for development

```
npm run build-dev
```

Built files are placed in `./dist/development`.

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

Vue configuration files for production and development are available in
`.env` and `.env.development`, respectively. The following environment
variables are recognized:

* `VUE_APP_API_URL` is the URL of the API server root endpoint. For example,
    in development mode this value is set to `VUE_APP_API_URL=http://localhost:8000`.
