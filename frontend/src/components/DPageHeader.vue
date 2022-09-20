<template>
  <DBreadcrumb :title="breadcrumbTitle ? breadcrumbTitle : title" />
  <DPageTitle :title="title" :subtitle="subtitle ? subtitle : undefined" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DBreadcrumb from "@/components/DBreadcrumb.vue"; // @ is an alias to /src
import DPageTitle from "@/components/DPageTitle.vue"; // @ is an alias to /src

export default defineComponent({
  name: "DPageHeader",
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
    DBreadcrumb,
    DPageTitle,
  },
});
</script>
