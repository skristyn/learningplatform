<template>
  <Breadcrumb :pageTitle="pageTitle" />
  <PageTitle :pageTitle="pageTitle" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Breadcrumb from "@/components/Breadcrumb.vue"; // @ is an alias to /src
import PageTitle from "@/components/PageTitle.vue"; // @ is an alias to /src

export default defineComponent({
  name: "PageHeader",
  props: {
    pageTitle: {
      required: true,
      type: String,
    },
  },
  components: {
    Breadcrumb,
    PageTitle,
  },
});
</script>
