<template>
  <nav class="breadcrumb-container" aria-label="Breadcrumbs">
    <!-- home icon -->
    <router-link to="/" class="home">
      <ion-icon name="home-outline"></ion-icon>
    </router-link>

    <!-- optional parent component breadcrumb -->
    <!-- ... to add this to the breadcrumbs, 
    add a breadcrumbTrail: BreadcrumbTrail object to meta in router/index.ts -->
    <template v-if="breadcrumbTrail">
      <span class="divider">></span>
      <router-link :to="{ name: breadcrumbTrail.routeName }">{{
        breadcrumbTrail.crumbTitle
      }}</router-link>
    </template>

    <!-- current page -->
    <span class="divider">></span>
    <p>{{ title }}</p>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useRoute } from "vue-router";
import { BreadcrumbTrail } from "@/types/BreadcrumbTrail";

export default defineComponent({
  name: "DBreadcrumb",
  props: {
    title: {
      required: true,
      type: String,
    },
  },
  setup() {
    const route = useRoute();

    // get the parent breadcrumb trail if available (if defined in router/index.ts)
    const breadcrumbTrail = route.matched[0].meta
      .breadcrumbTrail as BreadcrumbTrail;
    return { breadcrumbTrail };
  },
});
</script>

<style scoped>
.breadcrumb-container {
  display: flex;
  align-items: center;
}

.home {
  display: flex;
  font-size: 35px;
}

.divider {
  margin: 0 10px;
}
</style>
