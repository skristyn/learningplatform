<template>
  <h1 class="title">{{ title }}</h1>
  <h3 class="subtitle" v-if="subtitle">{{ subtitle }}</h3>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "DPageTitle",
  props: {
    title: {
      required: true,
      type: String,
    },
    subtitle: {
      type: String,
    },
  },
});
</script>

<style scoped>
.title {
  font-family: "Tourney", cursive;
  font-weight: 700;
  font-size: 2.8rem;
  color: var(--var-color-teal);
}

.subtitle {
  font-weight: normal;
  margin-top: -17px;
}
</style>
