<template>
  <PageHeader pageTitle="Sandbox SUB page" />
  <p>
    sub sandbox page. breadcrumb trail should have a crumb between home and the
    current component
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src

export default defineComponent({
  name: "SandboxSub",
  components: {
    PageHeader,
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
</style>
