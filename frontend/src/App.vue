<template>
  <div id="app">
    <component :is="this.$route.meta.layout || 'div'">
      <router-view />
    </component>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
});
</script>

<style>
/* Global styles go here */

/* CSS variables that can be used in other places */
:root {
  --var-color-almost-black: #2c3e50;
  --var-color-gray: gray;
  --var-color-gray-lighter: rgb(236, 240, 245);
  --var-color-green: #8ac38c;
  --var-color-green-light: #badcbb;
  --var-color-green-lighter: #d0e7d0;
  --var-color-teal: rgb(29, 148, 163);
}

html,
body {
  overflow: auto;
}

body {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--var-color-almost-black);
}

main {
  padding: 40px;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: var(--var-color-almost-black);
}

#nav a.router-link-exact-active {
  color: #42b983;
}

ion-icon {
  color: var(--var-color-gray);
}
</style>
