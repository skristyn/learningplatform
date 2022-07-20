<template>
  <PageHeader pageTitle="Digital Steward Training" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src

export default defineComponent({
  name: "CourseDashboard",
  components: {
    PageHeader,
  },
});
</script>
