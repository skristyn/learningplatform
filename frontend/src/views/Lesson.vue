<template>
  <p v-if="!currentSlide">Loading...</p>
  <div v-else>
    <LessonSlide :slide="currentSlide" :image="currentImage" />
  </div>
</template>

<script lang="ts">
import store from "@/store";
import { computed, defineComponent, reactive, toRefs, watch } from "vue";
import LessonSlide from "@/components/LessonSlide.vue";

export default defineComponent({
  name: "Lesson",
  components: { LessonSlide },
  props: {
    sectionId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    // get the current section to display
    store.dispatch("getCurrentSection", props.sectionId);

    // set the index of the slide to display from the section
    const state = reactive({ currentIndex: 0 });

    // set the current slide to display based on the set index
    const currentSlide = computed(
      () => store.state.currentSection?.slides[state.currentIndex]
    );

    // whenever currentSlide changes, fetch the image for the slide
    // TODO verify that slides always have an image
    watch(currentSlide, (newValue) => {
      store.dispatch("getCurrentImage", newValue?.value.image);
    });

    // get the image to display from global state
    const currentImage = computed(() => store.state.currentImage);

    return { ...toRefs(state), currentSlide, currentImage };
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
</style>
