<template>
  <div>
    <Header />
    <main>
      <slot />
    </main>
  </div>
</template>

<script>
import Header from "@/components/Header.vue"; // @ is an alias to /src

export default {
  name: "MainLayout",
  components: { Header },
};
</script>
