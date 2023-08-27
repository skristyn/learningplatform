<template>
  <!-- TODO verify that there aren't any other possible layout 'type's -->
  <!-- TODO verify that these layouts match the intention of the 'type's -->
  <!-- TODO verify if any other layouts can have a heading -->
  <div
    v-if="slide.type === 'headlineleftimage'"
    class="fadeIn headlineleftimage"
  >
    <img class="slideImage" :src="image_src" :alt="image?.title" />
    <div>
      <h2 v-if="slide?.value.heading">
        {{ slide.value.heading }}
      </h2>
      <span v-html="slide?.value.body"></span>
    </div>
  </div>

  <div
    v-else-if="slide.type === 'imagerightblock'"
    class="fadeIn imagerightblock"
  >
    <div>
      <span v-html="slide?.value.body"></span>
    </div>
    <img class="slideImage" :src="image_src" :alt="image?.title" />
  </div>

  <div v-else-if="slide.type === 'imagetopblock'" class="fadeIn imagetopblock">
    <img class="slideImage" :src="image_src" :alt="image?.title" />
    <div>
      <span v-html="slide?.value.body"></span>
    </div>
  </div>
  <button v-if="isLastSlide" @click="markComplete" class="markCompleteButton">
    Mark lesson complete
  </button>
</template>

<script lang="ts">
import store from "@/store";
import { Slide } from "@/types/Section";
import SlideImage from "@/types/SlideImage";
import { computed, defineComponent, PropType } from "vue";

export default defineComponent({
  name: "LessonSlide",
  props: {
    slide: {
      type: Object as PropType<Slide>,
      required: true,
    },
    slideIndex: {
      type: Number,
    },
    image: {
      type: Object as PropType<SlideImage | null>,
      required: true, // TODO verify that slides always have an image
    },
  },
  setup(props) {
    const image_src = computed(
      // TODO update this URL when the files are hosted elsewhere
      () => process.env.VUE_APP_API_URL + props.image?.meta.download_url
    );

    const isLastSlide = computed(
      () =>
        props.slideIndex ===
        (store.state.currentSection?.slides.length || 0) - 1
    );

    const markComplete = () => {
      // the button says "lesson", but this action is done on sections (see store/index.ts)
      store.dispatch("markSectionComplete");
    };

    return { image_src, isLastSlide, markComplete };
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
.headlineleftimage,
.imagerightblock,
.imagetopblock {
  margin-bottom: 20px;
  height: 100%;
  overflow-y: auto;
}

.headlineleftimage,
.imagerightblock {
  display: flex;
  flex-flow: row nowrap;
}

.imagetopblock {
  display: flex;
  flex-flow: column nowrap;
}

.headlineleftimage img {
  margin-right: 30px;
}

.imagerightblock img {
  margin-left: 30px;
}

.markCompleteButton {
  width: fit-content;
  margin: auto;
}

/* styles to fade in the slides */
.fadeIn {
  animation: fadeIn 0.4s;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
