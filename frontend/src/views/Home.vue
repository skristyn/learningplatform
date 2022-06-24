<template>
  <PageTitle pageTitle="Welcome!" />
  <div class="home">
    <p>home page placeholder</p>
    <p>for testing, can put links to other main pages here</p>
  </div>
  <div id="nav">
    <router-link to="/about"
      >The default "About" that Vue builds (keeping for testing)</router-link
    ><br />
    <router-link to="/lesson">Test lesson page</router-link><br />
    <router-link to="/sandbox">Testing sandbox page</router-link><br />
    <!-- <router-link to="/coursedashboard"
      >Testing course dashboard page</router-link
    > -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PageTitle from "@/components/PageTitle.vue";

export default defineComponent({
  name: "Home",
  components: {
    PageTitle,
  },
});
</script>
