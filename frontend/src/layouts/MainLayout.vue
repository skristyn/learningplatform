<template>
  <div class="mainContainer" :class="{ mainBackground: needsMainBackground }">
    <SiteHeader />
    <main>
      <slot />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import SiteHeader from "@/components/SiteHeader.vue"; // @ is an alias to /src

export default defineComponent({
  name: "MainLayout",
  components: { SiteHeader },
  computed: {
    needsMainBackground() {
      const needsMainBackground =
        this.$route.name == "Login" || this.$route.name == "Home";
      return needsMainBackground;
    },
  },
});
</script>

<style scoped>
.mainContainer {
  height: 100%;
}

.mainBackground {
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' height='100%25' width='100%25'%3E%3Cdefs%3E%3Cpattern id='doodad' width='75' height='75' viewBox='0 0 40 40' patternUnits='userSpaceOnUse' patternTransform='rotate(90)'%3E%3Crect width='100%25' height='100%25' fill='rgba(255, 255, 255, 1)'/%3E%3Cpath d='M-0.5 20v20h1v-20zM19.5 20v20h1v-20zM39.5 20v20h1v-20z' fill='rgba(255, 253, 213, 1)'/%3E%3Cpath d='M-10 29.5 h60 v1 h-60z' fill='rgba(255, 253, 213, 1)'/%3E%3Cpath d='M9.5 0v40h1v-40zM29.5 0v40h1v-40z' fill='rgba(255, 253, 213, 1)'/%3E%3Cpath d='M-10 9.5h60v1h-60z' fill='rgba(255, 253, 213, 1)'/%3E%3Cpath d='M-0.5 0v20h1v-20zM19.5 0v20h1v-20zM39.5 0v20h1v-20z' fill='rgba(255, 253, 213, 1)'/%3E%3C/pattern%3E%3C/defs%3E%3Crect fill='url(%23doodad)' height='200%25' width='200%25'/%3E%3C/svg%3E ");
}
</style>
