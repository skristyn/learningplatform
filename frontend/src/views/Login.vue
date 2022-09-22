<template>
  <DPageTitle title="Hi! We’re glad you’re here." />

  <div class="loginForm">
    <h2>Here for class?</h2>
    <form @submit="logIn">
      <input type="text" /><br />
      <input type="password" /><br />
      <button>Sign In</button>
    </form>
  </div>

  <h2>Want to know more?</h2>
  <p>
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Labore sequi natus
    delectus eligendi similique quia aperiam hic alias id sit tempora molestias
    rerum dolorem omnis recusandae, vel soluta officia voluptate!
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import DPageTitle from "@/components/DPageTitle.vue";

export default defineComponent({
  name: "Login",
  components: {
    DPageTitle,
  },
  methods: {
    async logIn() {
      this.$store.dispatch("logIn");
    },
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
.loginForm {
  text-align: center;
}

.title {
  font-size: 3em;
}
</style>
