<template>
  <DPageHeader title="Sanbox testing page" />
  <p>this is a page for testing things</p>

  <router-link :to="{ name: 'SandboxSub' }">
    link to subpage for testing breadcrumbs
  </router-link>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DPageHeader from "@/components/DPageHeader.vue"; // @ is an alias to /src

export default defineComponent({
  name: "Sandbox",
  components: {
    DPageHeader,
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
</style>
