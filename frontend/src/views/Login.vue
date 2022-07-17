<template>
  <PageTitle pageTitle="Hi! We’re glad you’re here." />
  <h2>Here for class?</h2>
  <!-- <form action=""> -->
  <form @submit="logIn">
    <input type="text" /><br />
    <input type="password" /><br />
    <button>Sign In</button>
  </form>
  <!-- TODO: sign in should actually authenticate user and not just redirect to /home -->

  <h2>Want to know more?</h2>
  <p>
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Labore sequi natus
    delectus eligendi similique quia aperiam hic alias id sit tempora molestias
    rerum dolorem omnis recusandae, vel soluta officia voluptate!
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import PageTitle from "@/components/PageTitle.vue";

export default defineComponent({
  name: "Login",
  components: {
    PageTitle,
  },
  methods: {
    async logIn() {
      if (!this.$store.state.isAuthenticated) {
        await this.$store.commit("logIn");

        if (this.$store.state.isAuthenticated) {
          this.$router.push({ name: "Home" });
        }
      }
    },
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
</style>
