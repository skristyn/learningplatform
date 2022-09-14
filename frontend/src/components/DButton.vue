<template>
  <router-link v-if="to" class="linkButton" :to="to">{{ text }}</router-link>
  <!-- TODO add a v-else that will create a button with an onclick -->
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { RouteLocationRaw } from "vue-router";

export default defineComponent({
  name: "DButton",
  props: {
    text: {
      type: String,
      required: true,
    },
    // the button either links to another page...
    to: {
      type: Object as PropType<RouteLocationRaw>,
      required: false,
    },
    // ... or it executes an action
    // TODO add a prop that will take an on-click fuction
  },
});
</script>

<style scoped>
.linkButton {
  display: inline-block; /* needed to add padding to this <a> tag */
  font-size: 26px;
  font-weight: bold;
  background: white;
  border: 2px solid var(--var-color-pink);
  border-radius: 10px;
  filter: drop-shadow(1px 2px 1px var(--var-color-pink));
  padding: 18px 96px;
}

/* prevent default link text decoration */
.linkButton:link,
.linkButton:visited,
.linkButton:hover,
.linkButton:active {
  text-decoration: none;
  color: var(--var-color-almost-black);
}
</style>
