<template>
  <div>
    <div class="navBar">
      <button
        class="navButton"
        :class="currentIndex === 0 ? 'hideButton' : ''"
        aria-label="Click to go to the previous slide"
        alt="Back button"
        title="Previous"
        @click="currentIndex === 0 ? undefined : onNavigate(currentIndex - 1)"
      >
        <ion-icon name="chevron-back-outline"></ion-icon>
        <p>Previous</p>
      </button>
      <button
        class="navButton"
        :class="currentIndex === slidesCount - 1 ? 'hideButton' : ''"
        aria-label="Click to go to the next slide"
        alt="Forward button"
        title="Next"
        @click="
          currentIndex === slidesCount - 1
            ? undefined
            : onNavigate(currentIndex + 1)
        "
      >
        <p>Next</p>
        <ion-icon name="chevron-forward-outline"></ion-icon>
      </button>
    </div>
    <div class="progressBar">
      <!-- TODO make these icons accessible -->
      <button
        v-for="(n, idx) in slidesCount"
        :key="idx"
        @click="onNavigate(idx)"
      >
        <ion-icon
          :name="`${n === slidesCount ? 'star' : 'ellipse'}${
            idx > currentIndex ? '-outline' : ''
          }`"
        ></ion-icon>
      </button>
      <!-- <ion-icon name="star-outline" v-for="idx"></ion-icon> -->
      <!-- <div class="circle" v-for="(n, idx) in slidesCount" :key="idx">
        {{ idx }}
      </div> -->
    </div>
  </div>
</template>

<script lang="ts">
import store from "@/store";
import { computed } from "@vue/reactivity";
import { defineComponent } from "vue";

export default defineComponent({
  name: "LessonFooter",
  props: {
    currentIndex: {
      type: Number,
      required: true,
    },
  },
  setup(props, { emit }) {
    const slidesCount = computed(
      () => store.state.currentSection?.slides.length || 0
    );

    const onNavigate = (index: number) => {
      // emit the "onSelectTab" event with the given tab title
      emit("onNavigate", index);
    };

    return { slidesCount, onNavigate };
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/

/* hide the default pointer events and hover titles */
ion-icon {
  pointer-events: none;
}

/* hide the default styles for the buttons */
button {
  background: none;
  border: none;
  cursor: pointer;
}

.hideButton {
  visibility: hidden;
}

.navBar {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
}

.navButton {
  display: flex;
  align-items: center;
  cursor: pointer;
  min-width: 1px;
}

.navButton p {
  font-size: 20px;
  margin: 0;
}

.navButton ion-icon {
  font-size: 62px;
  color: var(--var-color-green);
}

.progressBar {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center;
}

.progressBar ion-icon {
  font-size: 30px;
  --ionicon-stroke-width: 42px;
  color: var(--var-color-green);
  cursor: pointer;
}
</style>
