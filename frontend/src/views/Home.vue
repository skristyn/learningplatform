<template>
  <PageTitle pageTitle="Welcome!" />
  <div class="home">
    <router-link to="/course-dashboard">Go to course dashboard</router-link>
  </div>
  <div v-if="user">{{ user.announcement }}</div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PageTitle from "@/components/PageTitle.vue";

export default defineComponent({
  name: "Home",
  components: {
    PageTitle,
  },
  async mounted() {
    this.$store.dispatch("getUserData");
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
});
</script>
