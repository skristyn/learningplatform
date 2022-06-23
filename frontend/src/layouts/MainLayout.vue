<template>
  <div>
    <Header />
    <main>
      <slot />
    </main>
  </div>
</template>

<script lang="ts">
import Header from "@/components/Header.vue"; // @ is an alias to /src

export default {
  name: "MainLayout",
  components: { Header },
};
</script>
