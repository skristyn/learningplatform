<template>
  <Breadcrumb :title="breadcrumbTitle ? breadcrumbTitle : title" />
  <PageTitle :title="title" :subtitle="subtitle ? subtitle : undefined" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Breadcrumb from "@/components/Breadcrumb.vue"; // @ is an alias to /src
import PageTitle from "@/components/PageTitle.vue"; // @ is an alias to /src

export default defineComponent({
  name: "PageHeader",
  props: {
    title: {
      required: true,
      type: String,
    },
    subtitle: {
      type: String,
    },
    breadcrumbTitle: {
      type: String,
    },
  },
  components: {
    Breadcrumb,
    PageTitle,
  },
});
</script>
