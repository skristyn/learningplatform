<template>
<div class="login-grid">
  <div class="row">
    <h1 class="title">Hi! We’re glad you’re here.</h1>
  </div>
  <div class="form-row">
    <div class="loginForm">
      <h2>Here for class?</h2>
      <form @submit="logIn">
        <input type="text" /><br />
        <input type="password" /><br />
        <button>Sign In</button>
      </form>
    </div>
  </div>

  <div class="row">
    <h2>Want to know more?</h2>
    <p>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Labore sequi natus
      delectus eligendi similique quia aperiam hic alias id sit tempora molestias
      rerum dolorem omnis recusandae, vel soluta officia voluptate!
    </p>
  </div>
</div> <!-- end grid div -->
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Login",
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
  text-align: left;
  display: inline-block;
}

button {
  float: right;
}

.title {
  font-size: 3em;
  font-family: "Tourney", cursive;
  font-weight: 700;
  color: var(--var-color-teal);
}

.login-grid {
  display: grid;
  grid-template-columns: 1em 1fr 1em;
  column-gap: 1rem;
  row-gap: 5rem;
}

@media screen and (min-width: 950px) {
  .login-grid {
    grid-template-columns: minmax(10px, 1fr) minmax(100px, 4fr) minmax(10px, 1fr);
  }
}

div.row {
  grid-column: 2 / span 1;
}

.form-row {
  grid-column: 2 / span 1;
  justify-self: center;
}

</style>
