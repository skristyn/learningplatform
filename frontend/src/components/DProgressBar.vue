<template>
  <div class="container">
    <p class="title" id="progressbar-label">{{ title }}</p>
    <div
      class="progress"
      role="progressbar"
      aria-labelledby="progressbar-label"
      aria-valuemin="0"
      :aria-valuenow="percentComplete"
      aria-valuemax="100"
    >
      <div class="progressFill" :style="{ width: percentComplete + '%' }"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "DProgressBar",
  props: {
    title: {
      type: String,
      required: true,
    },
    percentComplete: {
      type: Number,
      required: true,
    },
  },
});
</script>

<style scoped>
.container {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  margin-bottom: 44px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  margin: 0 40px 0 0;
}

.progress {
  border: 2px solid var(--var-color-teal);
  border-radius: 30px;
  overflow: hidden;
  height: 38px;
  width: 100%;
}

.progressFill {
  height: 100%;
  background-color: var(--var-color-teal);
}
</style>
