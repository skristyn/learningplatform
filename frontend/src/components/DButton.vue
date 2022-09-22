<template>
  <router-link v-if="to" class="linkButton" :class="size || `small`" :to="to">{{
    text
  }}</router-link>
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
    size: {
      type: String as PropType<"large" | "small">,
      required: false,
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
/* 'small' is the default size */
.small {
  max-width: 440px;
  font-size: 22px;
  padding: 18px 36px;
}

.large {
  max-width: 800px;
  font-size: 26px;
  padding: 18px 96px;
}

.linkButton {
  display: inline-block; /* needed to add padding to this <a> tag */
  font-weight: bold;
  background: white;
  border: 2px solid var(--var-color-pink);
  border-radius: 10px;
  filter: drop-shadow(2px 3px 2px var(--var-color-pink));

  /* limit the text to one line, clip overflow with an ellipsis */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  /* apply any hover effects with a smooth transition */
  transition: all 0.2s ease;
}

.linkButton:hover {
  background-color: var(--var-color-pink-lighter);
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
