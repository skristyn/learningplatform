<template>
  <div class="lesson">
    <LessonSidebar />
    <main>
      <slot />
    </main>
  </div>
</template>

<script>
import LessonSidebar from "@/components/LessonSidebar.vue"; // @ is an alias to /src

export default {
  name: "LessonLayout",
  components: { LessonSidebar },
};
</script>

<style scoped>
.lesson {
  display: flex;
  height: 100vh;
}

main {
  width: 100%;
}
</style>
