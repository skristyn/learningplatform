<template>
  <h1>{{ pageTitle }}</h1>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "PageTitle",
  props: {
    pageTitle: {
      required: true,
      type: String,
    },
  },
});
</script>

<style scoped>
h1 {
  font-family: "Tourney", cursive;
  font-weight: 700;
  font-size: 40px;
  color: rgb(29, 148, 163);
}
</style>
