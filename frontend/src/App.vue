<template>
  <!-- TODO: possibly get rid of appInner -->
  <div id="appInner" class="test">
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
  --var-color-blue-dark: #3f679c;
  --var-color-gray: #878787;
  --var-color-gray-lighter: rgb(236, 240, 245);
  --var-color-green: #8ac38c;
  --var-color-green-light: #badcbb;
  --var-color-green-lighter: #d0e7d0;
  --var-color-teal: #19a3b2;
  --var-color-blue-dark: #3f679c;
  --var-color-pink: #f15882;
  --var-color-pink-light: #f9d0db;
  --var-color-pink-lighter: #fdecf1;
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
  width: 100%;
  height: 100%;
}

#appInner {
  width: 100%;
  height: 100%;
}

main {
  padding: 40px;
}

h1 {
  font-size: 40px;
}

h2 {
  font-size: 26px;
}

h3 {
  font-size: 24px;
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
